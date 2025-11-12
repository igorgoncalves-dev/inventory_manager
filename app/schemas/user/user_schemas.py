from datetime import datetime
from pydantic import BaseModel, EmailStr, Field, computed_field

class UserBaseSchema(BaseModel):
    name: str = Field(..., min_length=1)
    surname: str = Field(..., min_length=1)
    email: EmailStr
    

class CreateUserSchema(UserBaseSchema):
    status: bool = Field(default=False)
    admin: bool = Field(default=False)
    password: str | None = Field(None, min_length=8)

    cost_center: str | None = None
    machine_id: int | None = None
    smartphone_id: int | None = None
    
    class Config:
        json_schema_extra = {
            "user.example": {
                "name": "John",
                "surname": "Doe",
                "email": "john.doe@domain.com",
                "cost_center": "1.0.0",
                "status": True,
            }
        }

class CreateUserSchemaResponse(BaseModel):
    name: str
    surname: str
    email: str
    created_at: datetime

    @computed_field
    @property
    def display_name(self) -> str:
        return f"{self.name.capitalize()} {self.surname.capitalize()}"
    
    class Config:
        orm_mode = True
        
        json_schema_extra = {
            "name": "John",
            "surname": "Doe",
            "display_name": "John Doe",
            "email": "john.doe@mail.com",
            "machine_id": 10,
            "created_at": "2025-11-12T21:14:47"
        }

class UpdateUserSchema(CreateUserSchema):
    status: bool | None = None
    admin: bool | None = None
    password: str | None = None

    name: str | None = None
    surname: str | None = None
    email: EmailStr | None = None
    cost_center: str | None = None

    class Config:
        orm_mode = True