from sqlalchemy import Column, String, DateTime, Text, Integer, ForeignKey, JSON
from sqlalchemy.sql import func
from app.db.base import Base


class Material(Base):
    __tablename__ = "materials"

    id = Column(String, primary_key=True, index=True)  # UUID as string
    query_id = Column(String, ForeignKey("queries.id"), nullable=False)
    content_json = Column(JSON, nullable=False)  # Stores the generated content structure
    file_paths = Column(JSON, nullable=False)  # Stores paths to generated HTML/PDF files
    version = Column(Integer, nullable=False, default=1)  # For tracking iterations
    created_at = Column(DateTime(timezone=True), server_default=func.now())