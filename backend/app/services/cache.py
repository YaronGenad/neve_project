"""
Redis-backed cache service.

All operations degrade gracefully when Redis is unavailable – the caller
never needs to check `cache.available` before calling a method; every
method simply returns None/False instead of raising.
"""
import hashlib
import json
import pickle
from typing import Any, Dict, List, Optional, Tuple

import redis

from app.core.config import settings

# ── TTLs ──────────────────────────────────────────────────────────────────────
QUERY_TTL = 24 * 3600           # 24 hours
MATERIAL_TTL = 7 * 24 * 3600   # 7 days
USER_HISTORY_TTL = 30 * 24 * 3600  # 30 days
BM25_INDEX_TTL = 3600           # 1 hour


def _make_redis_client(url: str) -> Optional[redis.Redis]:
    """Try to create and ping a Redis client; return None on failure."""
    try:
        client: redis.Redis = redis.from_url(url, decode_responses=False, socket_connect_timeout=2)
        client.ping()
        return client
    except Exception:
        return None


class CacheService:
    def __init__(self, redis_client: Optional[redis.Redis] = None):
        # Allow injection of a fake/test client
        if redis_client is not None:
            self._client: Optional[redis.Redis] = redis_client
        else:
            self._client = _make_redis_client(settings.REDIS_URL)

    # ── availability ──────────────────────────────────────────────────────────

    @property
    def available(self) -> bool:
        return self._client is not None

    # ── key helpers ───────────────────────────────────────────────────────────

    @staticmethod
    def query_hash(subject: str, topic: str, grade: str, rounds: int) -> str:
        """Stable MD5 hash for a normalized query tuple."""
        normalized = (
            f"{subject.lower().strip()}"
            f"|{topic.lower().strip()}"
            f"|{grade.lower().strip()}"
            f"|{rounds}"
        )
        return hashlib.md5(normalized.encode("utf-8")).hexdigest()

    # ── query cache ───────────────────────────────────────────────────────────

    def get_cached_query(self, query_hash: str) -> Optional[Dict[str, Any]]:
        """Return cached generation result dict, or None."""
        if not self.available:
            return None
        try:
            raw = self._client.get(f"query:{query_hash}")
            return json.loads(raw) if raw else None
        except Exception:
            return None

    def cache_query(self, query_hash: str, result: Dict[str, Any]) -> bool:
        """Store a generation result. Returns True on success."""
        if not self.available:
            return False
        try:
            self._client.setex(
                f"query:{query_hash}",
                QUERY_TTL,
                json.dumps(result, default=str).encode("utf-8"),
            )
            return True
        except Exception:
            return False

    def invalidate_query(self, query_hash: str) -> bool:
        """Remove a cached query result."""
        if not self.available:
            return False
        try:
            self._client.delete(f"query:{query_hash}")
            return True
        except Exception:
            return False

    # ── material cache ────────────────────────────────────────────────────────

    def get_cached_material(self, material_id: str) -> Optional[Dict[str, Any]]:
        if not self.available:
            return None
        try:
            raw = self._client.get(f"material:{material_id}")
            return json.loads(raw) if raw else None
        except Exception:
            return None

    def cache_material(self, material_id: str, content: Dict[str, Any]) -> bool:
        if not self.available:
            return False
        try:
            self._client.setex(
                f"material:{material_id}",
                MATERIAL_TTL,
                json.dumps(content, default=str).encode("utf-8"),
            )
            return True
        except Exception:
            return False

    # ── user history cache ────────────────────────────────────────────────────

    def get_user_history(self, user_id: str) -> Optional[List]:
        if not self.available:
            return None
        try:
            raw = self._client.get(f"user:{user_id}:history")
            return json.loads(raw) if raw else None
        except Exception:
            return None

    def cache_user_history(self, user_id: str, history: List) -> bool:
        if not self.available:
            return False
        try:
            self._client.setex(
                f"user:{user_id}:history",
                USER_HISTORY_TTL,
                json.dumps(history, default=str).encode("utf-8"),
            )
            return True
        except Exception:
            return False

    def invalidate_user_history(self, user_id: str) -> bool:
        if not self.available:
            return False
        try:
            self._client.delete(f"user:{user_id}:history")
            return True
        except Exception:
            return False

    # ── BM25 index cache ──────────────────────────────────────────────────────

    def store_bm25_index(self, index_bytes: bytes, query_ids: List[str]) -> bool:
        """Persist serialized BM25 index + query ID list."""
        if not self.available:
            return False
        try:
            pipe = self._client.pipeline()
            pipe.setex("bm25:index", BM25_INDEX_TTL, index_bytes)
            pipe.setex(
                "bm25:query_ids",
                BM25_INDEX_TTL,
                json.dumps(query_ids).encode("utf-8"),
            )
            pipe.execute()
            return True
        except Exception:
            return False

    def get_bm25_index(self) -> Optional[Tuple[bytes, List[str]]]:
        """Return (index_bytes, query_ids) or None if not cached / expired."""
        if not self.available:
            return None
        try:
            index_bytes = self._client.get("bm25:index")
            ids_raw = self._client.get("bm25:query_ids")
            if not index_bytes or not ids_raw:
                return None
            return index_bytes, json.loads(ids_raw)
        except Exception:
            return None

    def invalidate_bm25_index(self) -> None:
        """Force next BM25 lookup to rebuild from DB."""
        if not self.available:
            return
        try:
            self._client.delete("bm25:index")
            self._client.delete("bm25:query_ids")
        except Exception:
            pass
