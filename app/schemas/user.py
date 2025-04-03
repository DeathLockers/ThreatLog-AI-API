from pydantic import BaseModel, EmailStr, Field


class UserBase(BaseModel):
  id: str
  name: str = Field(min_length=3, max_length=50)
  email: EmailStr


class UserCreateSeeder(UserBase):
  hashed_password: str


class User(UserBase):
  class Config:
    from_attributes = True
