from pydantic import BaseModel, EmailStr, Field

class UserBaseSchema(BaseModel):
    name: str = Field(..., min_length=1)
    surname: str = Field(..., min_length=1)
    email: EmailStr
    

class CreateUserSchema(UserBaseSchema):
    cost_center: str = Field(..., min_length=1)
    machine_id: int | None = None
    smartphone_id: int | None = None
    
    class Config:
        json_schema_extra = {
            "user.example": {
                "name": "John",
                "surname": "Doe",
                "email": "john.doe@domain.com",
                "cost_center": "1.0.0"
            }
        }


class UpdateUserSchema(UserBaseSchema):
    name: str | None = None
    surname: str | None = None
    email: EmailStr | None = None
    cost_center: str | None = None
    machine_id: int | None = None
    smartphone_id: int | None = None
    status: bool | None = None


class UserResponseSchema(UserBaseSchema):    
    
    id: int
    cost_center: str
    status: bool
    machine_id: int | None = None
    smartphone_id: int | None = None

    class Config:
        orm_mode = True

        json_schema_extra = {
            "email": "john.doe@domain.com",
            "display_name": "John Doe"
        }