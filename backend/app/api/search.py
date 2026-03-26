"""
Similarity-search endpoint.

GET /search/?q=<text>&top_k=5&threshold=1.0
Returns past completed generations whose BM25 score >= threshold.

Intended to be called as the teacher types their query so the UI can
surface "similar materials already generated" before triggering a new
(expensive) generation.
"""
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.api.dependencies import get_current_user
from app.db.session import get_db
from app.models.user import User
from app.services.search import (
    DEFAULT_SIMILARITY_THRESHOLD,
    DEFAULT_TOP_K,
    SearchService,
    build_query_text,
    create_search_service,
)

router = APIRouter()


@router.get("/")
def search_similar(
    q: str = Query(..., min_length=1, description="Free-text query (subject + topic + grade)"),
    subject: str = Query(default="", description="Filter: subject"),
    topic: str = Query(default="", description="Filter: topic"),
    grade: str = Query(default="", description="Filter: grade"),
    rounds: int = Query(default=4, ge=1, le=10, description="Rounds (used to build query text)"),
    top_k: int = Query(default=DEFAULT_TOP_K, ge=1, le=20),
    threshold: float = Query(default=DEFAULT_SIMILARITY_THRESHOLD, ge=0.0),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
    search_service: SearchService = Depends(create_search_service),
):
    """
    Find past generations similar to the provided query text.

    Pass `q` as a combined free-text string (e.g. "מדעים תאים ה-ו") or use
    the structured `subject`/`topic`/`grade`/`rounds` parameters which will be
    concatenated automatically.
    """
    if subject or topic or grade:
        query_text = build_query_text(subject, topic, grade, rounds)
    else:
        query_text = q

    results = search_service.find_similar(
        query_text=query_text,
        db=db,
        top_k=top_k,
        threshold=threshold,
    )

    return {
        "query": query_text,
        "threshold": threshold,
        "count": len(results),
        "results": results,
    }


@router.post("/rebuild-index")
def rebuild_bm25_index(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
    search_service: SearchService = Depends(create_search_service),
):
    """
    Force-rebuild the BM25 index from the current DB state.
    Useful after bulk imports or when the cache has expired.
    """
    search_service.invalidate_index()
    index, query_ids = search_service.build_index_from_db(db)
    if index is not None:
        search_service._persist_index(index, query_ids)

    return {
        "status": "rebuilt",
        "indexed_queries": len(query_ids),
        "cache_available": search_service.cache.available,
    }
