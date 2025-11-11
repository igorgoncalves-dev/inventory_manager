from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, null
from database import Base


class Machine(Base):

    __tablename__ = "machines"

    id = Column(Integer, primary_key=True, unique=True, autoincrement=True)
    hostname = Column(String(10), unique=True, nullable=False)
    type = Column(String(50))
    brand = Column(String(50), nullable=False) 
    model = Column(String(50), nullable=False)
    mac_address = Column(String(50), unique=True)
    mac_address_wifi = Column(String(50), unique=True)
    serial_number = Column(String(25), unique=True, nullable=False)
    cpu = Column(String(10))
    ram = Column(String(10))
    storage_1 = Column(String(10))
    storage_2 = Column(String(10))
    location = Column(String(2), default=None)
    user_id = Column(Integer, ForeignKey("users.id"), unique=True, default=None)
    is_active = Column(Boolean, nullable=False, default=True)
    status = Column(String, nullable=False, default="AVAILABLE" )


    