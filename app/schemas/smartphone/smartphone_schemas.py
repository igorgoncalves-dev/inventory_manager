from typing import Optional
from pydantic import BaseModel, Field

from utils.enum.machine_status import DeviceStatus

class SmartphoneBaseSchema(BaseModel):
    brand: str = Field(..., min_length=1, max_length=25)
    model: str = Field(..., min_length=1, max_length=25)
    storage: str = Field(..., min_length=1, max_length=25)
    ram: str = Field(..., min_length=1, max_length=25)
    imei: str = Field(..., min_length=1, max_length=25)
    number: Optional[str] = Field(None, min_length=11, max_length=11, description="Numero do CHIP com 11 digitos XX-XXX-XXX-XXX")
    pin_1: Optional[str] = Field(None, min_length=4, max_length=4, description="PIN 1 do Chip")
    pin_2: Optional[str] = Field(None, min_length=4, max_length=4, description="PIN 2 do Chip")
    puk_1: Optional[str] = Field(None, min_length=4, max_length=4, description="PUK 1 do Chip")
    puk_2: Optional[str] = Field(None, min_length=4, max_length=4, description="PUK 2 do Chip")
    location: str = Field(..., min_length=2, max_length=2, description="Localização")
    user_id: Optional[int] = None
    is_active: bool = True
    status: Optional[DeviceStatus] = Field(..., min_length=1, max_length=10, description="Situação atual do dispositivo")


class CreateSmartphoneSchema(SmartphoneBaseSchema):
    
    class Config:
        orm_mode = True

        json_extra_schema = {
        "brand": "Samsung" ,
        "model": "A04" ,
        "storage": "64GB" ,
        "ram": "4GB" ,
        "imei": "XXXXXXXXXXXXXXXXXXXXXX" ,
        "number": "DDXXXXXXXXX",
        "pin_1": "1234" ,
        "pin_2": "5678" ,
        "puk_1": "9182" ,
        "puk_2": "8291" ,
        "location": "SP" ,
        "user_id": 1 ,
        "is_active": True ,
        "status": "AVAILABLE" ,
        }


class UpdateSmartphoneSchema(SmartphoneBaseSchema):

    brand: Optional[str] = None
    model: Optional[str] = None
    storage: Optional[str] = None
    ram: Optional[str] = None
    imei: Optional[str] = None
    number: Optional[str] = None
    pin_1: Optional[str] = None
    pin_2: Optional[str] = None
    puk_1: Optional[str] = None
    puk_2: Optional[str] = None
    location: Optional[str] = None
    user_id: Optional[int] = None
    is_active: Optional[bool] = None
    status: Optional[DeviceStatus] = None

    class Config:
        orm_mode = True


class ResponseSmartphoneSchema(BaseModel):

    brand: str
    model: str
    storage: str
    ram: str
    imei: str
    number: str | None
    pin_1: str | None
    pin_2: str | None
    puk_1: str | None
    puk_2: str | None
    location: str

    class Config:
        orm_mode = True
