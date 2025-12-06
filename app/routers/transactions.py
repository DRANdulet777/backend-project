from fastapi import APIRouter, Depends, UploadFile, File, HTTPException
from typing import List
from sqlmodel import Session, select
from app.db import engine
from app.models import Transaction, Category
from app.auth import get_current_user
from app.schemas import TransactionCreate, TransactionRead
import pandas as pd
from datetime import datetime

router = APIRouter()


@router.post("/", response_model=TransactionRead)
def create_transaction(payload: TransactionCreate, current_user=Depends(get_current_user)):
    dt = payload.date
    with Session(engine) as session:
        tx = Transaction(amount=payload.amount, date=dt, description=payload.description, category_id=payload.category_id, user_id=current_user.id)
        session.add(tx)
        session.commit()
        session.refresh(tx)
        return tx


@router.get("/", response_model=List[TransactionRead])
def list_transactions(current_user=Depends(get_current_user)):
    with Session(engine) as session:
        statement = select(Transaction).where(Transaction.user_id == current_user.id)
        results = session.exec(statement).all()
        return results


@router.post('/import-csv')
def import_csv(file: UploadFile = File(...), current_user=Depends(get_current_user)):
    content = file.file.read()
    df = pd.read_csv(pd.io.common.BytesIO(content))
    created = 0
    with Session(engine) as session:
        for _, row in df.iterrows():
            # ожидаем колонки: date, amount, description, category
            try:
                dt = pd.to_datetime(row['date']).date()
                amount = float(row['amount'])
                description = str(row.get('description', ''))
                cat_name = row.get('category')
            except Exception:
                continue
            category_id = None
            if cat_name:
                statement = select(Category).where(Category.name == cat_name, Category.user_id == current_user.id)
                cat = session.exec(statement).first()
                if not cat:
                    cat = Category(name=cat_name, user_id=current_user.id)
                    session.add(cat)
                    session.commit()
                    session.refresh(cat)
                category_id = cat.id
            tx = Transaction(amount=amount, date=dt, description=description, category_id=category_id, user_id=current_user.id)
            session.add(tx)
            created += 1
        session.commit()
    return {"created": created}


@router.get('/report/monthly')
def monthly_report(year: int, month: int, current_user=Depends(get_current_user)):
    from sqlalchemy import extract
    with Session(engine) as session:
        statement = select(Transaction).where(Transaction.user_id == current_user.id)
        results = session.exec(statement).all()
        total = sum([t.amount for t in results if t.date.year == year and t.date.month == month])
        return {"year": year, "month": month, "total": total}
