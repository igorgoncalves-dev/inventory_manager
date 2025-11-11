from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from database import Base

class Smartphone(Base):

    __tablename__ = "smartphones"

    id = Column(Integer, primary_key=True, autoincrement=True)
    brand = Column(String(100), nullable=False) 
    model = Column(String(100), nullable=False) 
    storage = Column(Integer, nullable=False)
    ram = Column(Integer, nullable=False)
    imei = Column(String(50), nullable=False, unique=True)
    number = Column(String(15), unique=True)
    pin_1 = Column(String(10), default=None)
    pin_2 = Column(String(10), default=None)
    puk_1 = Column(String(10), default=None)
    puk_2 = Column(String(10), default=None)
    location = Column(String(2), default=None)
    user_id = Column(Integer, ForeignKey("users.id"), unique=True, default=None)
    is_active = Column(Boolean, nullable=False, default=True)
    status = Column(String, nullable=False, default="AVAILABLE" )

    def to_dict(self):
        return {
            "id": self.id,
            "brand": self.brand,
            "model": self.model,
            "storage": self.storage,
            "ram": self.ram,
            "imei": self.imei,
            "number": self.number,
            "pin_1": self.pin_1,
            "pin_2": self.pin_2,
            "puk_1": self.puk_1,
            "puk_2": self.puk_2,
            "location": self.location,
            "user_id": self.owner,
            "is_active": self.is_active,
            "status": self.status,
        }
