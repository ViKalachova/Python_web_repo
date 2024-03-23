from pydantic import BaseModel, EmailStr, Field, PastDate


class UserSchema(BaseModel):
    name: str = Field(min_length=2, max_length=50)
    surname: str = Field(min_length=2, max_length=50)
    email: EmailStr
    phone: str = Field()
    birthday: PastDate
    description: str = Field(max_length=250)

class UserResponse(BaseModel):
    id: int = 1
    name: str
    surname: str
    email: EmailStr
    phone: str
    birthday: PastDate
    description: str

    class Config:
        from_attributes = True
