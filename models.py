# models.py
from sqlalchemy import Column, Integer, String, DateTime, func, Text
from database import Base

class SearchHistory(Base):
    __tablename__ = "search_history"

    id = Column(Integer, primary_key=True, index=True)
    query = Column(Text, nullable=False)
    response = Column(Text, nullable=True)
    endpoint = Column(String(100), nullable=True)  # e.g., "chat", "summarize", ...
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
