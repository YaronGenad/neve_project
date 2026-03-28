from sqlalchemy import Column, String, DateTime, Text, Integer, ForeignKey, JSON, LargeBinary
from sqlalchemy.sql import func
from app.db.base import Base


class Material(Base):
    __tablename__ = "materials"

    id = Column(String, primary_key=True, index=True)  # UUID as string
    query_id = Column(String, ForeignKey("queries.id", ondelete="CASCADE"), nullable=False)
    content_json = Column(JSON, nullable=False)  # Stores the generated content structure
    file_paths = Column(JSON, nullable=False)  # Stores paths to generated HTML/PDF files
    version = Column(Integer, nullable=False, default=1)  # For tracking iterations

    # Denormalised for search (copied from parent Query at creation time)
    subject = Column(String(100), nullable=True)
    topic = Column(String(255), nullable=True)
    grade = Column(String(20), nullable=True)

    # Approval / usage counters (4.5)
    approval_count = Column(Integer, nullable=False, default=0, server_default="0")
    times_served = Column(Integer, nullable=False, default=0, server_default="0")

    # embedding (vector(768)) and fts_vector (tsvector) live in Postgres only —
    # managed by migration + trigger; not declared in ORM to stay DB-agnostic in tests.
    # Use raw SQL for reads/writes of these columns.

    created_at = Column(DateTime(timezone=True), server_default=func.now())