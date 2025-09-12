from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.sql import func
from database import Base

class User(Base):
    __tablename__ = "users"
    id = Column("id",Integer, autoincrement=True, primary_key=True, index=True)
    role_id = Column("role_id",Integer,ForeignKey("roles.id"), nullable=False)
    name = Column("name", String, nullable=False)
    email = Column("email", String, unique=True, index=True, nullable=False)
    password = Column("password", String, nullable=False)
    created_at = Column("created_at", DateTime(timezone=True), server_default=func.now())