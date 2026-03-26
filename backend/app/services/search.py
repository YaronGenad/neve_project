"""
BM25-based similarity search service.

Uses the rank-bm25 library to find past queries that are similar to a
new incoming query.  The BM25 index is serialised with pickle and cached
in Redis so it survives restarts and avoids rebuilding on every request.

Hebrew / Arabic text is handled correctly because BM25 operates on
whitespace-separated tokens – no language-specific stemming is required.
"""
import pickle
import re
from typing import Any, Dict, List, Optional, Tuple

from rank_bm25 import BM25Okapi
from sqlalchemy.orm import Session

from app.models.query import Query
from app.services.cache import CacheService

# ── constants ─────────────────────────────────────────────────────────────────

DEFAULT_SIMILARITY_THRESHOLD = 1.0  # minimum BM25 score to surface as a hit
DEFAULT_TOP_K = 5


# ── text helpers ──────────────────────────────────────────────────────────────

def normalize_query(text: str) -> str:
    """
    Lowercase, strip leading/trailing whitespace, collapse internal
    whitespace to a single space.  Hebrew text is unaffected by casing.
    """
    text = text.lower().strip()
    text = re.sub(r"\s+", " ", text)
    return text


def tokenize(text: str) -> List[str]:
    """Split normalized text into whitespace tokens."""
    return normalize_query(text).split()


def build_query_text(subject: str, topic: str, grade: str, rounds: int) -> str:
    """Canonical query string used for BM25 indexing and lookup."""
    return normalize_query(f"{subject} {topic} {grade} {rounds}")


# ── search service ────────────────────────────────────────────────────────────

class SearchService:
    """Stateless wrapper around BM25 + cache."""

    def __init__(self, cache_service: CacheService):
        self.cache = cache_service

    # ── index management ──────────────────────────────────────────────────────

    def build_index_from_db(
        self, db: Session
    ) -> Tuple[Optional[BM25Okapi], List[str]]:
        """
        Build a fresh BM25 index from all *completed* queries in the DB.
        Returns (index, query_id_list) – query_id[i] maps to corpus doc i.
        """
        queries = (
            db.query(Query)
            .filter(Query.status == "completed")
            .order_by(Query.created_at.asc())
            .all()
        )

        if not queries:
            return None, []

        corpus = [tokenize(q.query_text) for q in queries]
        query_ids = [q.id for q in queries]
        index = BM25Okapi(corpus)
        return index, query_ids

    def _persist_index(self, index: BM25Okapi, query_ids: List[str]) -> None:
        """Serialise and store the index in Redis."""
        try:
            self.cache.store_bm25_index(pickle.dumps(index), query_ids)
        except Exception:
            pass  # non-fatal – just won't be cached

    def get_or_build_index(
        self, db: Session
    ) -> Tuple[Optional[BM25Okapi], List[str]]:
        """
        Return the cached BM25 index if available, otherwise rebuild from DB
        and cache the result for future calls.
        """
        cached = self.cache.get_bm25_index()
        if cached:
            index_bytes, query_ids = cached
            try:
                return pickle.loads(index_bytes), query_ids
            except Exception:
                pass  # corrupt cache – fall through to rebuild

        index, query_ids = self.build_index_from_db(db)
        if index is not None:
            self._persist_index(index, query_ids)
        return index, query_ids

    def invalidate_index(self) -> None:
        """Force next call to rebuild the BM25 index."""
        self.cache.invalidate_bm25_index()

    # ── similarity search ─────────────────────────────────────────────────────

    def find_similar(
        self,
        query_text: str,
        db: Session,
        top_k: int = DEFAULT_TOP_K,
        threshold: float = DEFAULT_SIMILARITY_THRESHOLD,
    ) -> List[Dict[str, Any]]:
        """
        Return up to *top_k* completed queries whose BM25 score against
        *query_text* is >= *threshold*, sorted by descending score.

        Each result dict contains: generation_id, subject, topic, grade,
        rounds, similarity_score, created_at, status.
        """
        index, query_ids = self.get_or_build_index(db)

        if index is None or not query_ids:
            return []

        tokens = tokenize(query_text)
        scores = index.get_scores(tokens)

        # Pair IDs with scores and apply threshold
        pairs = [
            (query_ids[i], float(scores[i]))
            for i in range(len(query_ids))
            if scores[i] >= threshold
        ]
        pairs.sort(key=lambda x: x[1], reverse=True)
        pairs = pairs[:top_k]

        if not pairs:
            return []

        # Bulk-fetch query details from DB
        id_set = {p[0] for p in pairs}
        score_map = dict(pairs)
        rows = db.query(Query).filter(Query.id.in_(id_set)).all()

        results = [
            {
                "generation_id": row.id,
                "subject": row.subject,
                "topic": row.topic,
                "grade": row.grade,
                "rounds": row.rounds,
                "similarity_score": round(score_map[row.id], 4),
                "created_at": row.created_at,
                "status": row.status,
            }
            for row in rows
        ]
        # Re-sort because DB query doesn't preserve score order
        results.sort(key=lambda x: x["similarity_score"], reverse=True)
        return results


# ── dependency factories ──────────────────────────────────────────────────────

def create_cache_service() -> CacheService:
    return CacheService()


def create_search_service() -> SearchService:
    return SearchService(CacheService())
