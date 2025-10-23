from pydantic import BaseModel
from datetime import datetime

class PeriodMetricsBase(BaseModel):
    ticker_name: str
    period_type: str
    start_date: datetime
    end_date: datetime
    average_price: float 
    percentage_change: float
    simple_volatility: float 
    high_period: float
    low_period: float
    total_volume: int

class PeriodMetricsCreate(PeriodMetricsBase):
    pass

class PeriodMetricsResponse(PeriodMetricsBase):
    id: str
    created_at: datetime

    class Config:
        from_attributes = True