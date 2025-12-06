from typing import Optional
from datetime import date
from sqlmodel import SQLModel
from pydantic import EmailStr


class UserCreate(SQLModel):
    email: EmailStr
    password: str


class UserRead(SQLModel):
    id: int
    email: str


class CategoryCreate(SQLModel):
    name: str


class CategoryRead(SQLModel):
    id: int
    name: str


class TransactionCreate(SQLModel):
    amount: float
    date: date
    description: Optional[str] = None
    category_id: Optional[int] = None


class TransactionRead(SQLModel):
    id: int
    amount: float
    date: date
    description: Optional[str] = None
    category_id: Optional[int] = None
