from pydantic import BaseModel
from datetime import datetime

class HistoryBase(BaseModel):
    ticker_name: str
    open: float
    high: float
    low: float
    close: float
    volume: int
    dividends: float
    stock_splits: float
    date: datetime

class HistoryCreate(HistoryBase):
    pass

class HistoryResponse(HistoryBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True
