from datetime import datetime
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field


class GenerationRequest(BaseModel):
    subject: str = Field(..., min_length=1, max_length=200)
    topic: str = Field(..., min_length=1, max_length=500)
    grade: str = Field(..., min_length=1, max_length=20)
    rounds: int = Field(default=4, ge=1, le=10)
    force_new: bool = Field(
        default=False,
        description="Skip cache/similarity checks and always generate fresh materials",
    )


class SimilarQueryResult(BaseModel):
    generation_id: str
    subject: str
    topic: str
    grade: str
    rounds: int
    similarity_score: float
    created_at: Optional[datetime] = None
    status: str


class GenerationResponse(BaseModel):
    generation_id: str
    status: str
    message: str
    from_cache: bool = False
    similar_queries: List[SimilarQueryResult] = []


class GenerationStatusResponse(BaseModel):
    generation_id: str
    status: str
    created_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    subject: str
    topic: str
    grade: str
    rounds: int
    result: Optional[Dict[str, Any]] = None
    error: Optional[str] = None
    material_id: Optional[str] = None  # set when status == "completed"


class GenerationListItem(BaseModel):
    generation_id: str
    status: str
    created_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    subject: str
    topic: str
    grade: str
    rounds: int


class GenerationListResponse(BaseModel):
    generations: List[GenerationListItem]
    limit: int
    offset: int


# ── Approval / versions (Sprint 4.5) ─────────────────────────────────────────

class MaterialApprovalResponse(BaseModel):
    status: str           # "approved" | "rejected"
    material_id: str
    approval_count: Optional[int] = None


class MaterialVersionItem(BaseModel):
    material_id: str
    version: int
    approval_count: int
    times_served: int
    subject: str
    topic: str
    grade: str
    created_at: Optional[datetime] = None


class MaterialVersionsResponse(BaseModel):
    subject: str
    topic: str
    grade: str
    versions: List[MaterialVersionItem]
