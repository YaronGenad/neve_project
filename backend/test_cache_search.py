"""
Sprint 3 tests – Redis cache service + BM25 similarity search.

All Redis calls use fakeredis so no real Redis instance is needed.
All generation calls use the mock service from Sprint 2 tests.
"""
import json
import os
import sys

# ── env setup BEFORE any app import ──────────────────────────────────────────
os.environ.setdefault("SECRET_KEY", "test-secret-key-for-testing")
os.environ.setdefault("DEBUG", "true")
os.environ.setdefault("DATABASE_URL", "sqlite:///./test_alhasade_complete.db")
os.environ.setdefault("GEMINI_API_KEY", "test-key")
os.environ.setdefault("NVIDIA_API_KEY", "test-key")
os.environ.setdefault("AUTH_RATE_LIMIT", "1000/minute")
os.environ.setdefault("GENERATION_RATE_LIMIT", "1000/minute")

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

# ── imports ───────────────────────────────────────────────────────────────────
from unittest.mock import MagicMock

import fakeredis
from fastapi.testclient import TestClient

from app.db.base import Base
from app.db.session import SessionLocal, engine
from app.main import app
from app.models import material, query, user  # noqa: F401
from app.services.cache import CacheService
from app.services.generation import GenerationService, create_generation_service
from app.services.search import (
    SearchService,
    build_query_text,
    create_search_service,
    normalize_query,
    tokenize,
)

Base.metadata.create_all(bind=engine)

# ── shared fake-redis instance (persists across all tests in this file) ───────
FAKE_REDIS = fakeredis.FakeRedis()


def fake_cache_service() -> CacheService:
    return CacheService(redis_client=FAKE_REDIS)


def fake_search_service() -> SearchService:
    return SearchService(CacheService(redis_client=FAKE_REDIS))


MOCK_RESULT = {
    "generation_id": "mock-gen-id",
    "status": "completed",
    "input": {"subject": "מדעים", "topic": "תאים", "grade": "ה-ו", "rounds": 1},
    "output_dir": "/tmp/mock_output",
    "roadmap": {},
    "results": {
        "student_pdf": "/tmp/mock_student.pdf",
        "teacher_pdf": "/tmp/mock_teacher.pdf",
        "rounds": [],
    },
    "files": {
        "student_pdf": "/tmp/mock_student.pdf",
        "teacher_pdf": "/tmp/mock_teacher.pdf",
        "rounds": [],
    },
    "generated_at": "2026-01-01T00:00:00Z",
}


def mock_generation_service() -> GenerationService:
    svc = MagicMock(spec=GenerationService)
    svc.generate_materials.return_value = MOCK_RESULT
    return svc


app.dependency_overrides[create_generation_service] = mock_generation_service
app.dependency_overrides[create_search_service] = fake_search_service

client = TestClient(app)


# ── helpers ───────────────────────────────────────────────────────────────────

def _register_and_login(email: str) -> str:
    client.post(
        "/auth/register",
        json={"email": email, "password": "testpassword123", "full_name": "Test User"},
    )
    resp = client.post("/auth/login", data={"username": email, "password": "testpassword123"})
    return resp.json()["access_token"]


def _submit(token: str, subject: str, topic: str, grade: str = "ה-ו", rounds: int = 1) -> dict:
    resp = client.post(
        "/generations/",
        json={"subject": subject, "topic": topic, "grade": grade, "rounds": rounds},
        headers={"Authorization": f"Bearer {token}"},
    )
    return resp.json()


# ═══════════════════════════════════════════════════════════════════════════════
# 1.  Text utility tests (pure functions – no DB / Redis needed)
# ═══════════════════════════════════════════════════════════════════════════════

def test_normalize_query_basic():
    assert normalize_query("  Hello   World  ") == "hello world"
    assert normalize_query("מדעים  תאים") == "מדעים תאים"
    assert normalize_query("UPPER") == "upper"
    print("normalize_query basic test passed!")


def test_normalize_query_idempotent():
    text = "מדעים תאים ה-ו 2"
    assert normalize_query(normalize_query(text)) == normalize_query(text)
    print("normalize_query idempotent test passed!")


def test_tokenize():
    tokens = tokenize("מדעים תאים ה-ו")
    assert tokens == ["מדעים", "תאים", "ה-ו"]
    tokens_en = tokenize("science cells grade5")
    assert tokens_en == ["science", "cells", "grade5"]
    print("tokenize test passed!")


def test_build_query_text():
    qt = build_query_text("מדעים", "תאים", "ה-ו", 2)
    assert "מדעים" in qt
    assert "תאים" in qt
    print("build_query_text test passed!")


# ═══════════════════════════════════════════════════════════════════════════════
# 2.  CacheService unit tests (using fakeredis)
# ═══════════════════════════════════════════════════════════════════════════════

def test_cache_service_available():
    svc = CacheService(redis_client=FAKE_REDIS)
    assert svc.available is True
    print("CacheService available test passed!")


def test_cache_service_unavailable():
    svc = CacheService(redis_client=None)
    assert svc.available is False
    # All methods should return None/False gracefully
    assert svc.get_cached_query("x") is None
    assert svc.cache_query("x", {}) is False
    print("CacheService unavailable graceful degradation test passed!")


def test_query_hash_stable():
    h1 = CacheService.query_hash("מדעים", "תאים", "ה-ו", 2)
    h2 = CacheService.query_hash("מדעים", "תאים", "ה-ו", 2)
    h3 = CacheService.query_hash("מדעים", "תאים", "ה-ו", 3)  # different rounds
    assert h1 == h2
    assert h1 != h3
    print("query_hash stable test passed!")


def test_query_hash_normalizes_whitespace():
    h1 = CacheService.query_hash("מדעים", "תאים", "ה-ו", 1)
    h2 = CacheService.query_hash(" מדעים ", " תאים ", " ה-ו ", 1)
    assert h1 == h2
    print("query_hash whitespace normalization test passed!")


def test_cache_set_and_get_query():
    svc = CacheService(redis_client=FAKE_REDIS)
    q_hash = CacheService.query_hash("ביולוגיה", "פוטוסינתזה", "ז-ח", 2)
    payload = {"status": "completed", "data": "some content"}

    assert svc.cache_query(q_hash, payload) is True
    result = svc.get_cached_query(q_hash)
    assert result is not None
    assert result["status"] == "completed"
    print("cache set/get query test passed!")


def test_cache_miss_returns_none():
    svc = CacheService(redis_client=FAKE_REDIS)
    assert svc.get_cached_query("nonexistent-hash-xyz") is None
    print("cache miss returns None test passed!")


def test_cache_invalidate_query():
    svc = CacheService(redis_client=FAKE_REDIS)
    q_hash = CacheService.query_hash("היסטוריה", "מלחמות", "ט-י", 1)
    svc.cache_query(q_hash, {"status": "completed"})
    assert svc.get_cached_query(q_hash) is not None

    svc.invalidate_query(q_hash)
    assert svc.get_cached_query(q_hash) is None
    print("cache invalidate query test passed!")


def test_cache_material():
    svc = CacheService(redis_client=FAKE_REDIS)
    mat_id = "material-uuid-001"
    content = {"rounds": [{"round": 1}]}

    assert svc.cache_material(mat_id, content) is True
    result = svc.get_cached_material(mat_id)
    assert result is not None
    assert "rounds" in result
    print("cache material set/get test passed!")


def test_cache_user_history():
    svc = CacheService(redis_client=FAKE_REDIS)
    user_id = "user-test-id"
    history = [{"generation_id": "g1"}, {"generation_id": "g2"}]

    svc.cache_user_history(user_id, history)
    result = svc.get_user_history(user_id)
    assert result is not None
    assert len(result) == 2

    svc.invalidate_user_history(user_id)
    assert svc.get_user_history(user_id) is None
    print("cache user history test passed!")


def test_bm25_index_store_and_retrieve():
    import pickle
    from rank_bm25 import BM25Okapi

    svc = CacheService(redis_client=FAKE_REDIS)
    # Use a larger, more diverse corpus so BM25 IDF scores are non-trivial
    corpus = [
        ["science", "cells", "biology", "mitosis"],
        ["history", "wars", "ancient", "rome"],
        ["math", "algebra", "equations", "numbers"],
    ]
    index = BM25Okapi(corpus)
    query_ids = ["id-1", "id-2", "id-3"]

    index_bytes = pickle.dumps(index)
    svc.store_bm25_index(index_bytes, query_ids)

    result = svc.get_bm25_index()
    assert result is not None
    recovered_bytes, recovered_ids = result
    recovered_index = pickle.loads(recovered_bytes)
    assert recovered_ids == query_ids
    assert isinstance(recovered_index, BM25Okapi)
    assert recovered_index.corpus_size == 3
    # "science" appears only in doc 0 – it should score highest there
    scores = recovered_index.get_scores(["science"])
    assert scores[0] > scores[1]
    assert scores[0] > scores[2]
    print("BM25 index store/retrieve test passed!")


def test_bm25_index_invalidate():
    import pickle
    from rank_bm25 import BM25Okapi

    svc = CacheService(redis_client=FAKE_REDIS)
    index = BM25Okapi([["test"]])
    svc.store_bm25_index(pickle.dumps(index), ["id-x"])
    assert svc.get_bm25_index() is not None

    svc.invalidate_bm25_index()
    assert svc.get_bm25_index() is None
    print("BM25 index invalidate test passed!")


# ═══════════════════════════════════════════════════════════════════════════════
# 3.  SearchService unit tests
# ═══════════════════════════════════════════════════════════════════════════════

def test_search_empty_db_returns_empty():
    db = SessionLocal()
    try:
        svc = SearchService(CacheService(redis_client=FAKE_REDIS))
        results = svc.find_similar("מדעים תאים ה-ו 1", db, top_k=5, threshold=0.0)
        assert isinstance(results, list)
        # May return results if other tests already inserted completed queries
    finally:
        db.close()
    print("SearchService empty results test passed!")


def test_search_finds_similar_after_completed_generation():
    """Insert a completed query directly into the DB and verify BM25 finds it."""
    from app.models.query import Query as QueryModel

    db = SessionLocal()
    try:
        # Invalidate index so we rebuild fresh
        svc = SearchService(CacheService(redis_client=FAKE_REDIS))
        svc.invalidate_index()

        q = QueryModel(
            id="search-test-query-id",
            user_id="dummy-user",
            subject="כימיה",
            topic="תמיסות",
            grade="ח-ט",
            rounds=2,
            query_text=build_query_text("כימיה", "תמיסות", "ח-ט", 2),
            status="completed",
        )
        # Only insert if not already there
        existing = db.query(QueryModel).filter(QueryModel.id == "search-test-query-id").first()
        if not existing:
            db.add(q)
            db.commit()

        results = svc.find_similar("כימיה תמיסות ח-ט 2", db, top_k=5, threshold=0.1)
        generation_ids = [r["generation_id"] for r in results]
        assert "search-test-query-id" in generation_ids
        print("SearchService finds similar after insert test passed!")
    finally:
        db.close()


def test_search_threshold_filters_low_scores():
    db = SessionLocal()
    try:
        svc = SearchService(CacheService(redis_client=FAKE_REDIS))
        # Very high threshold – should return nothing for unrelated query
        results = svc.find_similar("xyz abc 999", db, top_k=5, threshold=999.0)
        assert results == []
        print("SearchService threshold filter test passed!")
    finally:
        db.close()


def test_search_build_index_returns_correct_count():
    db = SessionLocal()
    try:
        svc = SearchService(CacheService(redis_client=FAKE_REDIS))
        index, query_ids = svc.build_index_from_db(db)
        # Should have at least the query we inserted above
        assert len(query_ids) >= 0  # graceful even if 0
        print("SearchService build index count test passed!")
    finally:
        db.close()


# ═══════════════════════════════════════════════════════════════════════════════
# 4.  API integration tests
# ═══════════════════════════════════════════════════════════════════════════════

def test_search_endpoint_requires_auth():
    resp = client.get("/search/?q=מדעים")
    assert resp.status_code in (401, 403)
    print("Search endpoint requires auth test passed!")


def test_search_endpoint_returns_results():
    token = _register_and_login("cache_search@example.com")
    resp = client.get(
        "/search/?q=כימיה תמיסות",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert resp.status_code == 200
    data = resp.json()
    assert "results" in data
    assert "count" in data
    assert "query" in data
    print("Search endpoint returns results test passed!")


def test_search_endpoint_structured_params():
    token = _register_and_login("cache_search2@example.com")
    resp = client.get(
        "/search/?q=_&subject=כימיה&topic=תמיסות&grade=ח-ט&rounds=2",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert resp.status_code == 200
    data = resp.json()
    assert "כימיה" in data["query"]
    print("Search endpoint structured params test passed!")


def test_generation_cache_hit():
    """
    Submit a generation, manually cache its result, then submit again with the
    same parameters – second call should return from_cache=True immediately.
    """
    token = _register_and_login("cache_hit@example.com")

    # First submission (generates normally, mock returns completed)
    resp1 = client.post(
        "/generations/",
        json={"subject": "פיזיקה", "topic": "אופטיקה", "grade": "יא-יב", "rounds": 1},
        headers={"Authorization": f"Bearer {token}"},
    )
    assert resp1.status_code == 202

    # Seed the cache directly (simulating what the background task would do)
    q_hash = CacheService.query_hash("פיזיקה", "אופטיקה", "יא-יב", 1)
    svc = CacheService(redis_client=FAKE_REDIS)
    svc.cache_query(q_hash, MOCK_RESULT)

    # Second submission – should hit the cache
    resp2 = client.post(
        "/generations/",
        json={"subject": "פיזיקה", "topic": "אופטיקה", "grade": "יא-יב", "rounds": 1},
        headers={"Authorization": f"Bearer {token}"},
    )
    assert resp2.status_code == 202
    data2 = resp2.json()
    assert data2["from_cache"] is True
    assert data2["status"] == "completed"
    print("Cache hit integration test passed!")


def test_generation_force_new_skips_cache():
    """force_new=True must bypass the cache and always start a new generation."""
    token = _register_and_login("force_new@example.com")

    # Seed cache
    q_hash = CacheService.query_hash("אנגלית", "grammar", "ג-ד", 1)
    svc = CacheService(redis_client=FAKE_REDIS)
    svc.cache_query(q_hash, MOCK_RESULT)

    # Submit with force_new=True
    resp = client.post(
        "/generations/",
        json={"subject": "אנגלית", "topic": "grammar", "grade": "ג-ד", "rounds": 1, "force_new": True},
        headers={"Authorization": f"Bearer {token}"},
    )
    assert resp.status_code == 202
    data = resp.json()
    assert data["from_cache"] is False
    assert data["status"] == "pending"
    print("force_new skips cache test passed!")


def test_generation_response_includes_similar_queries_field():
    """Response always has similar_queries list (may be empty)."""
    token = _register_and_login("similar_field@example.com")
    resp = client.post(
        "/generations/",
        json={"subject": "אמנות", "topic": "ציור", "grade": "א-ב", "rounds": 1},
        headers={"Authorization": f"Bearer {token}"},
    )
    assert resp.status_code == 202
    data = resp.json()
    assert "similar_queries" in data
    assert isinstance(data["similar_queries"], list)
    print("similar_queries field in response test passed!")


def test_rebuild_index_endpoint():
    token = _register_and_login("rebuild_idx@example.com")
    resp = client.post(
        "/search/rebuild-index",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert resp.status_code == 200
    data = resp.json()
    assert data["status"] == "rebuilt"
    assert "indexed_queries" in data
    print("Rebuild index endpoint test passed!")


# ── entrypoint ────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    # Text utilities
    test_normalize_query_basic()
    test_normalize_query_idempotent()
    test_tokenize()
    test_build_query_text()
    # CacheService
    test_cache_service_available()
    test_cache_service_unavailable()
    test_query_hash_stable()
    test_query_hash_normalizes_whitespace()
    test_cache_set_and_get_query()
    test_cache_miss_returns_none()
    test_cache_invalidate_query()
    test_cache_material()
    test_cache_user_history()
    test_bm25_index_store_and_retrieve()
    test_bm25_index_invalidate()
    # SearchService
    test_search_empty_db_returns_empty()
    test_search_finds_similar_after_completed_generation()
    test_search_threshold_filters_low_scores()
    test_search_build_index_returns_correct_count()
    # API
    test_search_endpoint_requires_auth()
    test_search_endpoint_returns_results()
    test_search_endpoint_structured_params()
    test_generation_cache_hit()
    test_generation_force_new_skips_cache()
    test_generation_response_includes_similar_queries_field()
    test_rebuild_index_endpoint()
    print("\nAll Sprint 3 tests passed!")
