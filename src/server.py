from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from database import engine, get_db, Base
from userModel import User
from historyModel import History
from roleModel import Role

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Minha API", version="1.0.0")


@app.get("/")
def read_root():
    return {"message": "API funcionando"}


@app.get("/users/")
def get_users(db: Session = Depends(get_db)):
    users = db.query(User).all()
    return users


@app.post("/users/")
def create_user(name: str, email: str, password:str ,role_id: str ,db: Session = Depends(get_db)):
    existing_user = db.query(User).filter(User.email == email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email já cadastrado")

    new_user = User(name=name, email=email, password=password, role_id=role_id)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@app.post("/history/")
def create_history(
    ticker_name: str,
    open: float,
    high: float,
    low: float,
    close: float,
    volume: int,
    dividends: float,
    stock_splits: float,
    db: Session = Depends(get_db),
):
    new_history = History(
        ticker_name=ticker_name,
        open=open,
        high=high,
        low=low,
        close=close,
        volume=volume,
        dividends=dividends,
        stock_splits=stock_splits,
    )
    db.add(new_history)
    db.commit()
    db.refresh(new_history)
    return new_history

@app.get("/history/")
def get_history(db: Session = Depends(get_db)):
    history = db.query(History).all()
    return history

@app.post("/roles/")
def create_role(description: str, db: Session = Depends(get_db)):
    new_role = Role(description=description)
    db.add(new_role)
    db.commit()
    db.refresh(new_role)
    return new_role

@app.get("/roles/")
def get_roles(db: Session = Depends(get_db)):
    roles = db.query(Role).all()
    return roles
