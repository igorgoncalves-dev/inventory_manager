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

    """ # Class constructor
    def __init__(self, name, surname, email, cost_center, machine_id, smartphone_id, status=True):
        self.name = name
        self.surname = surname
        self.email = email
        self.cost_center = cost_center
        self.machine_id = machine_id
        self.smartphone_id = smartphone_id
        self.status = status """

    # JSON/DICT converter
    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "surname": self.surname,
            "email": self.email,
            "status": self.status,
            "cost_center": self.cost_center,
            "machine_id": self.machine_id,
            "smartphone_id": self.smartphone_id
        }