from typing import Optional
from datetime import date
from sqlmodel import SQLModel, Field
from sqlalchemy import Column, String


class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    # make email unique at DB level
    email: str = Field(sa_column=Column("email", String, unique=True, index=True))
    hashed_password: str


class Category(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    user_id: Optional[int] = Field(default=None, foreign_key="user.id")


class Transaction(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    amount: float
    date: date
    description: Optional[str] = None
    category_id: Optional[int] = Field(default=None, foreign_key="category.id")
    user_id: Optional[int] = Field(default=None, foreign_key="user.id")
