from sqlalchemy import Column, Integer, String, DateTime, Float
from sqlalchemy.sql import func
from database import Base

class History(Base):
    __tablename__ = "history"

    id = Column(Integer, autoincrement=True, primary_key=True, index=True)
    ticker_name = Column(String, nullable=False)
    open = Column(Float, nullable=False)
    high = Column(Float, nullable=False)
    low = Column(Float, nullable=False)
    close = Column(Float, nullable=False)
    volume = Column(Integer, nullable=False)
    dividends = Column(Float, nullable=False)  
    stock_splits = Column(Float, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
