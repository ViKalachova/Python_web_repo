from datetime import datetime

from pydantic import BaseModel, EmailStr, Field, PastDate, ConfigDict

from src.schemas.user import UserResponse


class ContactSchema(BaseModel):
    name: str = Field(min_length=2, max_length=50)
    surname: str = Field(min_length=2, max_length=50)
    email: EmailStr
    phone: str = Field()
    birthday: PastDate
    description: str = Field(max_length=250)

class ContactResponse(BaseModel):
    id: int = 1
    name: str
    surname: str
    email: EmailStr
    phone: str
    birthday: PastDate
    description: str
    created_at: datetime | None
    updated_at: datetime | None
    user: UserResponse | None
    model_config = ConfigDict(from_attributes=True)  # noqa
