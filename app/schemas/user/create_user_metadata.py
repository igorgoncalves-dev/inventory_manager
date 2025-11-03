from datetime import datetime
from pydantic import BaseModel, Field


class CreateUserMetadata(BaseModel):
    message: str = Field(min_length=1)
    created_at: datetime = Field(default_factory=datetime.now())
