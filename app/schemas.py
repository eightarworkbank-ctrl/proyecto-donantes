from __future__ import annotations

from datetime import date, datetime

from pydantic import BaseModel, ConfigDict, Field


class UserCreate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    name: str = Field(..., min_length=2, max_length=100)
    email: str
    password: str = Field(..., min_length=6, max_length=128)


class UserLogin(BaseModel):
    email: str
    password: str


class UserOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    email: str
    role: str
    is_active: bool
    created_at: datetime


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class DonorCreate(BaseModel):
    name: str = Field(..., min_length=2, max_length=100)
    blood_type: str = Field(..., min_length=2, max_length=10)
    city: str = Field(..., min_length=2, max_length=80)
    phone: str = Field(..., min_length=7, max_length=20)
    email: str | None = None
    last_donation: date | None = None


class DonorOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    blood_type: str
    city: str
    phone: str
    email: str | None
    last_donation: date | None
    created_at: datetime
