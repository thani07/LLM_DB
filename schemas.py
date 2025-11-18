# schemas.py
from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class ChatRequest(BaseModel):
    user_input: str

class SummaryRequest(BaseModel):
    text: str

class TranslationRequest(BaseModel):
    text: str
    target_Language: str

class SentimentRequest(BaseModel):
    text: str

class HistoryItem(BaseModel):
    id: int
    query: str
    response: Optional[str]
    endpoint: Optional[str]
    created_at: datetime

    class Config:
        orm_mode = True
