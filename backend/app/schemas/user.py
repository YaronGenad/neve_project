from typing import Optional

from pydantic import BaseModel, EmailStr, Field


class UserBase(BaseModel):
    email: EmailStr
    full_name: Optional[str] = None


class UserCreate(UserBase):
    password: str = Field(..., min_length=8)


class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    full_name: Optional[str] = None
    password: Optional[str] = None


class UserInDBBase(UserBase):
    id: str
    is_active: bool = True

    class Config:
        from_attributes = True


class UserInDB(UserInDBBase):
    """Internal schema that includes the hashed password – never returned to clients."""
    password_hash: str


class UserResponse(UserInDBBase):
    """Public user representation returned by API endpoints."""
    pass


class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class TokenPayload(BaseModel):
    sub: str  # user id
    exp: int


class RefreshTokenRequest(BaseModel):
    refresh_token: str
