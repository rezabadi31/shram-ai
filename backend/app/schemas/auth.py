from enum import Enum
from typing import Optional
from pydantic import BaseModel, Field


class RoleEnum(str, Enum):
    EMPLOYER = "employer"
    INSPECTOR = "inspector"
    ADMIN = "admin"


class UserLogin(BaseModel):
    email: str
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
    role: str
    name: str
    email: str


class TokenPayload(BaseModel):
    sub: Optional[str] = None
    role: Optional[str] = None
    name: Optional[str] = None


class UserResponse(BaseModel):
    id: str
    email: str
    name: str
    role: RoleEnum
    designation: str
    establishment_id: Optional[str] = None
    jurisdiction: Optional[str] = None
