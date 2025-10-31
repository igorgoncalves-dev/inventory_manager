from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from database import Base

class User(Base):

    # Database table name
    __tablename__ = "users"

    # Database columns and configurations
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    mail = Column(String(100), unique=True, nullable=False)
    status = Column(Boolean, nullable=False)
    cost_center = Column(String(10), nullable=False)
    machine_id = Column(Integer, unique=True)
    smartphone_id = Column(Integer, unique=True)

    # Class constructor
    def __init__(self, name, mail, cost_center, machine_id, smartphone_id, status=True):
        self.name = name
        self.mail = mail
        self.cost_center = cost_center
        self.machine_id = machine_id
        self.smartphone_id = smartphone_id
        self.status = status

    # JSON/DICT converter
    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "mail": self.mail,
            "status": self.status,
            "cost_center": self.cost_center,
            "machine_id": self.machine_id,
            "smartphone_id": self.smartphone_id
        }