from datetime import datetime
from fastapi import HTTPException
from pydantic import BaseModel, ConfigDict, EmailStr, Field, computed_field, model_validator

# BASE SCHEMAS
class UserBaseSchema(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    surname: str = Field(..., min_length=1, max_length=100)
    email: EmailStr

class UserOptionalBaseSchema(BaseModel):
    name: str | None = Field(None, min_length=1, max_length=100)
    surname: str | None = Field(None, min_length=1, max_length=100)
    email: EmailStr | None = None




# REQUESTS SCHEMA
class CreateUserRequest(UserBaseSchema):
    password: str | None = Field(None, min_length=8, max_length=100)
    
    cost_center: str | None = None
    machine_id: int | None = None
    smartphone_id: int | None = None
    
    status: bool = True
    admin: bool = False

    @model_validator(mode='after')
    def check_password_for_admin(self):

        """Valida que usuários admin sempre tenham senha"""
        if self.admin and not self.password:
            raise HTTPException(400, detail={"message": "Usuários administradores devem ter uma senha"})
        
        if self.password and not self.admin:
            raise HTTPException(400, detail={"message": "Senhas somente devem ser atribuídas a administradores"})
        return self

    model_config = ConfigDict(
        str_strip_whitespace=True,
        str_to_lower=True,

        json_schema_extra={
            "example": {
                "name": "John",
                "surname": "Doe",
                "email": "john.doe@domain.com",
                "cost_center": "1.0.0",
                "status": True,
                "admin": False
            }
        }
    )

class UpdateUserRequest(UserOptionalBaseSchema):
    password: str | None = Field(None, min_length=8, max_length=100)
    
    cost_center: str | None = None
    machine_id: int | None = None
    smartphone_id: int | None = None

    status: bool | None = None
    admin: bool | None = None

    @model_validator(mode="after")
    def check_password_for_admin(self):

        if self.admin and not self.password:
            raise HTTPException(400, detail={"message": "Não é possível criar um administrador sem uma senha"})
        
        if self.password and not self.admin:
            raise HTTPException(400, detail={"message": "Apenas usuários administradores podem conter senhas"})
        
        return self

    model_config = ConfigDict(
        str_strip_whitespace=True,
        str_to_lower=True,

        json_schema_extra={
            "example": {
                "name": "John",
                "surname": "Doe",
                "email": "john.doe@domain.com",
                "cost_center": None,
                "machine_id": None,
                "smartphone_id": 1,
                "status": False,
                "admin": False

            }
        }
    )



# RESPONSE SCHEMA
class UserResponseBase(UserBaseSchema):
    status: bool
    admin: bool
    timestamp: datetime

    @computed_field
    @property
    def display_name(self) -> str:
        return f"{self.name.capitalize()} {self.surname.capitalize()}"
    

class CreateUserResponse(UserResponseBase):
    message: str = "User has been created successfully!"

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "name": "John",
                "surname": "Doe",
                "email": "john.doe@domain.com",
                "status": True,
                "admin": False,
                "timestamp": "2025-01-15T10:30:00",
                "message": "User has been created succesfully!",
            }
        }
    )

class UpdateUserResponse(UserResponseBase):
    message: str = "User has been updated successfully!"

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "name": "John",
                "surname": "Doe",
                "email": "john.doe@domain.com",
                "status": True,
                "admin": False,
                "timestamp": "2025-01-15T10:30:00",
                "message": "User has been updated succesfully!",
            }
        }
    )