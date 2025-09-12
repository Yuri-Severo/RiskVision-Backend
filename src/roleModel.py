from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.sql import func
from database import Base

class Role(Base):
    __tablename__ = "roles"
    id = Column(Integer, primary_key=True, index=True)
    description = Column("description", String, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())