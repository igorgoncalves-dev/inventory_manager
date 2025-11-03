from pydantic import BaseModel, EmailStr, Field

from schemas.user.create_user_metadata import CreateUserMetadata


class CreateUser(BaseModel):
    name: str = Field(min_length=1, max_length=50)
    surname: str = Field(min_length=1, max_length=50)
    email: EmailStr
    cost_center: str = Field(min_length=1, max_length=50)

    class Config:
        schema_extra = {
            "user.example": {
                "name": "John",
                "surname": "Doe",
                "email": "john.doe@domain.com",
                "cost_center": "1.0.0"
            }
        }

class CreateUserResponse(BaseModel):
    
    # metadata: CreateUserMetadata
    email: EmailStr
    display_name: str

    class Config:
        orm_mode: True