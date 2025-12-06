from fastapi import APIRouter, Depends, HTTPException
from typing import List
from sqlmodel import Session, select
from app.db import engine
from app.models import Category
from app.auth import get_current_user
from app.schemas import CategoryCreate, CategoryRead

router = APIRouter()


@router.post("/", response_model=CategoryRead)
def create_category(payload: CategoryCreate, current_user=Depends(get_current_user)):
    with Session(engine) as session:
        cat = Category(name=payload.name, user_id=current_user.id)
        session.add(cat)
        session.commit()
        session.refresh(cat)
        return cat


@router.get("/", response_model=List[CategoryRead])
def list_categories(current_user=Depends(get_current_user)):
    with Session(engine) as session:
        statement = select(Category).where(Category.user_id == current_user.id)
        results = session.exec(statement).all()
        return results
