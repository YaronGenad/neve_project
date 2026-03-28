"""
File cleanup service — Sprint 5.

cleanup_old_files()  : deletes generated output files older than MAX_FILE_AGE_HOURS.
warm_cache()         : pre-populates Redis unit-ID lists for the top-50 requested topics.

Both functions are safe to call in a background thread or on a cron schedule.
They never raise — all exceptions are caught and logged.
"""
import time
from pathlib import Path
from typing import TYPE_CHECKING

from app.core.config import settings
from app.core.logging import get_logger
from app.services.cache import CacheService

if TYPE_CHECKING:
    from sqlalchemy.orm import Session

log = get_logger("app.services.cleanup")


# ── File cleanup ──────────────────────────────────────────────────────────────

def cleanup_old_files() -> dict:
    """
    Walk OUTPUT_DIR and delete files whose mtime is older than MAX_FILE_AGE_HOURS.

    Returns {"deleted": N, "errors": N}.
    """
    output_dir = Path(settings.OUTPUT_DIR)
    if not output_dir.exists():
        log.info("cleanup_skip", reason="output_dir_not_found", path=str(output_dir))
        return {"deleted": 0, "errors": 0}

    max_age_seconds = settings.MAX_FILE_AGE_HOURS * 3600
    now = time.time()
    deleted = 0
    errors = 0

    for file_path in output_dir.rglob("*"):
        if not file_path.is_file():
            continue
        try:
            age_seconds = now - file_path.stat().st_mtime
            if age_seconds > max_age_seconds:
                file_path.unlink()
                deleted += 1
        except Exception as exc:
            log.warning("cleanup_file_error", path=str(file_path), error=str(exc))
            errors += 1

    log.info("cleanup_complete", deleted=deleted, errors=errors)
    return {"deleted": deleted, "errors": errors}


# ── Cache warming ─────────────────────────────────────────────────────────────

def warm_cache(db: "Session") -> int:
    """
    Pre-populate Redis unit-ID lists for the top-50 most-requested topics.

    Reads the ``hot:units:top50`` sorted set and, for any topic whose
    ``unit:{subject}:{topic}:{grade}`` key is missing or expired, fetches
    the approval-sorted material IDs from Postgres and writes them to Redis.

    Returns the number of keys newly warmed.
    """
    cache = CacheService()
    if not cache.available:
        log.info("cache_warm_skip", reason="redis_unavailable")
        return 0

    try:
        # pylint: disable=protected-access
        top_keys = cache._client.zrevrange("hot:units:top50", 0, 49)
    except Exception as exc:
        log.warning("cache_warm_error", step="read_hot_set", error=str(exc))
        return 0

    warmed = 0
    for raw_key in top_keys:
        key_str = raw_key.decode() if isinstance(raw_key, bytes) else str(raw_key)
        parts = key_str.split(":", 2)
        if len(parts) != 3:
            continue
        subject, topic, grade = parts

        # Skip if already cached
        if cache.get_unit_ids(subject, topic, grade) is not None:
            continue

        try:
            from app.models.material import Material

            materials = (
                db.query(Material)
                .filter(
                    Material.subject == subject,
                    Material.topic == topic,
                    Material.grade == grade,
                )
                .order_by(Material.approval_count.desc())
                .all()
            )
            if materials:
                cache.set_unit_ids(subject, topic, grade, [m.id for m in materials])
                warmed += 1
        except Exception as exc:
            log.warning(
                "cache_warm_error",
                step="db_query",
                subject=subject,
                topic=topic,
                grade=grade,
                error=str(exc),
            )

    log.info("cache_warm_complete", warmed=warmed)
    return warmed
