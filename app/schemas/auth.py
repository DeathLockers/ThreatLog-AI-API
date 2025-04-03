from pydantic import BaseModel, EmailStr, Field


class Token(BaseModel):
  access_token: str
  token_type: str


class TokenData(BaseModel):
  username: str  # Email login


class Login(BaseModel):
  email: EmailStr
  password: str = Field(min_length=8)
