from sqlalchemy import Column, ForeignKey, Integer, String
from database import Base


class Machine(Base):

    __tablename__ = "machines"

    id = Column(Integer, primary_key=True, unique=True)
    hostname = Column(String(10), unique=True, nullable=False)
    type = Column(String(50)) 
    model = Column(String(100), nullable=False)
    mac_adress = Column(String(100))
    mac_adress_wifi = Column(String(100))
    serial_number = Column(String(100), unique=True, nullable=False)
    cpu = Column(String(100))
    ram = Column(String(100))
    storage_1 = Column(String(100))
    storage_2 = Column(String(100))
    location = Column(String(2), nullable=False)
    owner_id = Column(Integer, ForeignKey("users.id"))

    def to_dict(self):
        return {
            "hostname": self.hostname,
            "type": self.type,
            "model": self.model,
            "mac_adress": self.mac_adress,
            "mac_adress_wifi": self.mac_adress_wifi,
            "serial_number": self.serial_number,
            "cpu": self.cpu,
            "ram": self.ram,
            "storage_1": self.storage_1,
            "storage_2": self.storage_2,
            "location": self.location,
            "owner_id": self.owner_id,
        }

    