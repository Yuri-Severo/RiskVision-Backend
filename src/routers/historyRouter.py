from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from typing import Optional
from database import get_db
from models.historyModel import History
from schemas.historySchema import HistoryCreate, HistoryResponse

router = APIRouter(prefix="/history", tags=["History"])

@router.get("/", response_model=list[HistoryResponse])
def get_history(
    period: Optional[str] = Query(None, description="Filtro de período: day, week, semester, year"),
    db: Session = Depends(get_db)
):
    valid_periods = ["day", "week", "semester", "year"]
    
    if period is not None and period not in valid_periods:
        raise HTTPException(
            status_code=400,
            detail=f"Período inválido. Valores aceitos: {', '.join(valid_periods)}"
        )
    
    # Query base
    query = db.query(History)
    
    # Aplicar filtro de data se período foi especificado
    if period:
        now = datetime.now()
        
        if period == "day":
            start_date = now - timedelta(days=1)
        elif period == "week":
            start_date = now - timedelta(weeks=1)
        elif period == "semester":
            start_date = now - timedelta(days=180)  # ~6 meses
        elif period == "year":
            start_date = now - timedelta(days=365)
        
        query = query.filter(History.date >= start_date)
    
    return query.all()

@router.post("/", response_model=HistoryResponse)
def create_history(history: HistoryCreate, db: Session = Depends(get_db)):
    new_history = History(**history.dict())
    db.add(new_history)
    db.commit()
    db.refresh(new_history)
    return new_history
