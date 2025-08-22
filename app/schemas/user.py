from pydantic import BaseModel, EmailStr, Field
from typing import Optional, Literal

class UserBase(BaseModel):
    name: str = Field(min_length=1, max_length=255)
    email: EmailStr

class UserCreate(UserBase):
    password: str = Field(min_length=8, max_length=128)

class UserOut(BaseModel):
    id: str
    name: str
    email: EmailStr
    role: Literal["user", "admin"]

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    expires_in: int

class Pagination(BaseModel):
    page: int
    limit: int
    total: int

class UsersListResponse(Pagination):
    data: list[UserOut]
