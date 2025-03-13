from src.schemas import CustomBase
from datetime import datetime
from pydantic import PositiveInt, Field, EmailStr
from typing import Optional


class UserResponse(CustomBase):
    id: PositiveInt
    username: str = Field(..., min_length=5, max_length=30)
    email: EmailStr
    is_admin: bool
    created_at: datetime


class UserCreate(CustomBase):
    username: str = Field(..., min_length=5, max_length=30)
    email: EmailStr
    password: str = Field(..., min_length=5, max_length=30)
    is_admin: bool = Field(False)


class UserUpdate(CustomBase):
    username: Optional[str] = Field(None, min_length=5, max_length=30)
    email: Optional[EmailStr] = Field(None)
    password: Optional[str] = Field(None, min_length=5, max_length=30)
    is_admin: Optional[bool] = Field(None)


class UserLogin(CustomBase):
    username: Optional[str] = Field(None, min_length=5, max_length=30)
    password: Optional[str] = Field(None, min_length=5, max_length=30)
