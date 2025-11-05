from typing import Optional
from pydantic import BaseModel, Field

from utils.enum.machine_status import DeviceStatus

class MachineBaseSchema(BaseModel):

    hostname: str = Field(..., min_length=1, max_length=10)
    type: str = Field(..., min_length=1, max_length=25)
    brand: str = Field(..., min_length=1, max_length=25)
    model: str = Field(..., min_length=1, max_length=25)
    mac_address: Optional[str] = Field(None, min_length=1, max_length=50)
    mac_address_wifi: Optional[str] = Field(None, min_length=1, max_length=50)
    serial_number: str = Field(..., min_length=1, max_length=25)
    cpu: Optional[str] = Field(None, min_length=1, max_length=25, description="Processador")
    ram: Optional[str] = Field(None, description="RAM em GB")
    storage_1: Optional[str] = Field(None, description="Armazenamento primário em GB")
    storage_2: Optional[str] = Field(None, description="Armazenamento secundário em GB")
    location: str = Field(..., min_length=2, max_length=2, description="Localização")
    user_id: Optional[int] = None
    is_active: bool = True
    status: Optional[DeviceStatus] = Field(None, min_length=1, max_length=50, description="Situação atual do dispositivo")

    class Config:
        orm_mode = True

class CreateMachineSchema(MachineBaseSchema):

    class Config:
        orm_mode = True

        json_schema_extra = {
            "hostname": "ABC001234",
            "type": "Notebook",
            "brand": "Lenovo",
            "model": "Thinkpad E14",
            "mac_address": "XX:XX:XX:XX:XX:XX",
            "mac_address_wifi": "XX:XX:XX:XX:XX:XX",
            "serial_number": "ABC123456",
            "cpu": "Ryzen 5 5500",
            "ram": "16GB",
            "storage_1": "1TB",
            "location": "SP", 
            "user_id": 1,
            "is_active": True, 
            "status": "IN USE",
        }

class UpdateMachineSchema(MachineBaseSchema):
    hostname: Optional[str] = None
    type: Optional[str] = None
    brand: Optional[str] = None
    model: Optional[str] = None
    mac_address: Optional[str] = None
    mac_address_wifi: Optional[str] = None
    serial_number: Optional[str] = None
    cpu: Optional[str] = None
    ram: Optional[str] = None
    storage_1: Optional[str] = None
    storage_2: Optional[str] = None
    location: Optional[str] = None 
    user_id: Optional[int] = None
    is_active: Optional[bool] = None
    status: Optional[str] = None

    class Config:
        orm_mode = True

class ResponseMachineSchema(BaseModel):
    
    hostname: str
    type: str
    model: str
    serial_number: str
    cpu: str | None
    ram: str | None
    storage_1: str | None
    storage_2: str | None
    location: str

    class Config:
        orm_mode = True