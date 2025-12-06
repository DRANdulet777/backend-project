from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from datetime import timedelta
from sqlmodel import Session, select
from app.auth import authenticate_user, create_access_token, get_password_hash
from app.models import User
from app.db import engine
from app.schemas import UserCreate, UserRead

router = APIRouter()


@router.post("/register", response_model=UserRead)
def register(payload: UserCreate):
    with Session(engine) as session:
        statement = select(User).where(User.email == payload.email)
        existing = session.exec(statement).first()
        if existing:
            raise HTTPException(status_code=400, detail="Email already registered")
        user = User(email=payload.email, hashed_password=get_password_hash(payload.password))
        session.add(user)
        session.commit()
        session.refresh(user)
        return user


@router.post("/token")
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=401, detail="Incorrect username or password")
    access_token_expires = timedelta(minutes=60 * 24)
    access_token = create_access_token(data={"sub": user.email}, expires_delta=access_token_expires)
    return {"access_token": access_token, "token_type": "bearer"}
