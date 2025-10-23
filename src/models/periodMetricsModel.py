from sqlalchemy import Column, Integer, String, DateTime, Float
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from database import Base
import uuid

class History(Base):
    __tablename__ = "period_metrics"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    ticker_name = Column(String, nullable=False)
    period_type = Column(String, nullable=False)
    start_date = Column(DateTime(timezone=False), nullable=False)
    end_date = Column(DateTime(timezone=False), nullable=False)
    average_price = Column(Float, nullable=False)
    percentage_change = Column(Float, nullable=False)
    simple_volatility = Column(Float, nullable=False)
    high_period = Column(Float, nullable=False)
    low_period = Column(Float, nullable=False)
    total_volume = Column(Integer, nullable=False)
    created_at = Column(DateTime(timezone=False), server_default=func.now())
