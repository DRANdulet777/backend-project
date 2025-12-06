from fastapi import FastAPI
from app.db import init_db
from app.routers import auth, categories, transactions

app = FastAPI(title="Personal Finance Tracker")

app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(categories.router, prefix="/categories", tags=["categories"])
app.include_router(transactions.router, prefix="/transactions", tags=["transactions"])


@app.on_event("startup")
def on_startup():
    init_db()


@app.get("/")
def root():
    return {"message": "Personal Finance Tracker API"}
