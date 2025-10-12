from sqlalchemy import Column, Integer, String, DateTime, Float
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from database import Base
import uuid

class History(Base):
    __tablename__ = "history"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    ticker_name = Column(String, nullable=False)
    open = Column(Float, nullable=False)
    high = Column(Float, nullable=False)
    low = Column(Float, nullable=False)
    close = Column(Float, nullable=False)
    volume = Column(Integer, nullable=False)
    dividends = Column(Float, nullable=False)  
    stock_splits = Column(Float, nullable=False)
    date = Column(DateTime(timezone=False), nullable=False)
    created_at = Column(DateTime(timezone=False), server_default=func.now())
