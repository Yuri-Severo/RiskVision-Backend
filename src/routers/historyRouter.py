from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import Optional
from database import get_db
from models.historyModel import History
from schemas.historySchema import HistoryCreate, HistoryResponse, HistoryBase
from integrations.market_data.yfinance_client import get_yfinance_client
from core.config import TICKER

router = APIRouter(prefix="/history", tags=["History"])

@router.get("/")
def get_history(
    limit: Optional[int] = Query(100, description="Número máximo de registros"),
    db: Session = Depends(get_db)
):
    """
    Obtém histórico de preços diretamente do Yahoo Finance.
    Retorna dados dos últimos 30 dias com intervalo de 1 dia.
    """
    try:
        # Buscar dados diretamente do Yahoo Finance
        yf_client = get_yfinance_client()
        
        # Usar período de 30 dias com intervalo de 1 dia
        df = yf_client.get_history(period="30d", interval="1d")
        
        if df is None or df.empty:
            return []
        
        # Converter DataFrame para lista de dicionários
        df_reset = df.reset_index()
        
        # Limitar resultados
        if len(df_reset) > limit:
            df_reset = df_reset.tail(limit)
        
        # Formatar resposta
        result = []
        for idx, row in df_reset.iterrows():
            result.append({
                "id": int(idx) + 1,
                "ticker": TICKER,
                "date": row['Date'].isoformat() if hasattr(row['Date'], 'isoformat') else str(row['Date']),
                "open": float(row['Open']),
                "high": float(row['High']),
                "low": float(row['Low']),
                "close": float(row['Close']),
                "volume": int(row['Volume'])
            })
        
        return result
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao buscar histórico: {str(e)}")


@router.post("/", response_model=HistoryResponse)
def create_history(history: HistoryCreate, db: Session = Depends(get_db)):
    """Cria um novo registro de histórico no banco de dados."""
    new_history = History(**history.dict())
    db.add(new_history)
    db.commit()
    db.refresh(new_history)
    return new_history


@router.put("/{history_id}", response_model=HistoryResponse)
def update_history(history_id: int, history_data: HistoryBase, db: Session = Depends(get_db)):
    """Atualiza um registro de histórico existente."""
    history = db.query(History).filter(History.id == history_id).first()
    if not history:
        raise HTTPException(status_code=404, detail="Registro de histórico não encontrado")
    
    history.ticker_name = history_data.ticker_name
    history.open = history_data.open
    history.high = history_data.high
    history.low = history_data.low
    history.close = history_data.close
    history.volume = history_data.volume
    history.dividends = history_data.dividends
    history.stock_splits = history_data.stock_splits
    history.date = history_data.date
    
    db.commit()
    db.refresh(history)
    return history


@router.delete("/{history_id}")
def delete_history(history_id: int, db: Session = Depends(get_db)):
    """Deleta um registro de histórico."""
    history = db.query(History).filter(History.id == history_id).first()
    if not history:
        raise HTTPException(status_code=404, detail="Registro de histórico não encontrado")
    
    db.delete(history)
    db.commit()
    return {"message": "Registro de histórico deletado com sucesso"}
