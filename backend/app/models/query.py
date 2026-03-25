from sqlalchemy import Column, String, DateTime, Text, Integer, ForeignKey
from sqlalchemy.sql import func
from app.db.base import Base


class Query(Base):
    __tablename__ = "queries"

    id = Column(String, primary_key=True, index=True)  # UUID as string
    user_id = Column(String, ForeignKey("users.id"), nullable=False)
    subject = Column(String, nullable=False)
    topic = Column(String, nullable=False)
    grade = Column(String, nullable=False)
    rounds = Column(Integer, nullable=False)
    query_text = Column(Text, nullable=False)  # Normalized query for search
    created_at = Column(DateTime(timezone=True), server_default=func.now())