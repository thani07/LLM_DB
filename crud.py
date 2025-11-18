# crud.py
from sqlalchemy.orm import Session
from models import SearchHistory
from typing import List, Optional

def create_history(db: Session, query: str, response: Optional[str] = None, endpoint: Optional[str] = None) -> SearchHistory:
    item = SearchHistory(query=query, response=response, endpoint=endpoint)
    db.add(item)
    db.commit()
    db.refresh(item)
    return item

def get_history(db: Session, limit: int = 50, offset: int = 0) -> List[SearchHistory]:
    return db.query(SearchHistory).order_by(SearchHistory.created_at.desc()).offset(offset).limit(limit).all()

def get_history_by_id(db: Session, item_id: int) -> Optional[SearchHistory]:
    return db.query(SearchHistory).filter(SearchHistory.id == item_id).first()

def delete_history(db: Session, item_id: int) -> bool:
    obj = db.query(SearchHistory).filter(SearchHistory.id == item_id).first()
    if not obj:
        return False
    db.delete(obj)
    db.commit()
    return True
