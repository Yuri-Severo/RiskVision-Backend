from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Float
from sqlalchemy.sql import func
from database import Base

class History(Base):
    __tablename__ = "history"
    id = Column("id",Integer,autoincrement=True, primary_key=True, index=True)
    ticker_name = Column("name", String, nullable=False)
    open = Column("open", Float, nullable=False)
    high = Column("high", Float, nullable=False)
    low = Column("low", Float, nullable=False)
    close = Column("close", Float, nullable=False)
    volume = Column("volume", Integer, nullable=False)
    dividends = Column("dividends", Float, nullable=False)  
    stock_splits = Column("stock_splits", Float, nullable=False)
    created_at = Column("created_at",DateTime(timezone=True), server_default=func.now())