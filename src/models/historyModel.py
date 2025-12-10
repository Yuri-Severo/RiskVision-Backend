from sqlalchemy import Column, Integer, String, DateTime, Float, Index, UniqueConstraint
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
    date = Column(DateTime, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Índice composto para otimizar queries por ticker e data
    __table_args__ = (
        Index("idx_ticker_date", "ticker_name", "date"),
        UniqueConstraint("ticker_name", "date", name="uq_ticker_date"),
    )
