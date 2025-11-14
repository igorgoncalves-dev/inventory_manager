from email.policy import default
from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String, func
from database import Base

class User(Base):

    # Database table name
    __tablename__ = "users"

    # Database columns and configurations
    id = Column(Integer, primary_key=True, unique=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    surname = Column(String(100), nullable=False)
    password = Column(String(100), default=None)
    email = Column(String(100), unique=True, nullable=False)
    status = Column(Boolean, nullable=False, default=True)
    cost_center = Column(String(10))
    machine_id = Column(Integer, ForeignKey("machines.id"), unique=True, default=None)
    smartphone_id = Column(Integer, ForeignKey("smartphones.id"), unique=True, default=None)
    admin = Column(Boolean, nullable=False, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    blocked_at = Column(DateTime(timezone=True), default=None)