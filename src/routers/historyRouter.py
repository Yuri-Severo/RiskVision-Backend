from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
from models.historyModel import History
from schemas.historySchema import HistoryCreate, HistoryResponse

router = APIRouter(prefix="/history", tags=["History"])

@router.get("/", response_model=list[HistoryResponse])
def get_history(db: Session = Depends(get_db)):
    return db.query(History).all()

@router.post("/", response_model=HistoryResponse)
def create_history(history: HistoryCreate, db: Session = Depends(get_db)):
    new_history = History(**history.dict())
    db.add(new_history)
    db.commit()
    db.refresh(new_history)
    return new_history
