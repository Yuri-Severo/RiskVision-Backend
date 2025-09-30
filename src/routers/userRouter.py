import re
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models.userModel import User
from schemas.userSchema import UserCreate, UserResponse
from utils.security import hash_password,validate_password

router = APIRouter(prefix="/users", tags=["Users"])

@router.get("/", response_model=list[UserResponse])
def get_users(db: Session = Depends(get_db)):
    return db.query(User).all()

@router.post("/", response_model=UserResponse)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    existing_user = db.query(User).filter(User.email == user.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email já cadastrado")
    
    # Validação da senha guga
    if not validate_password(user.password):
        raise HTTPException(
            status_code=400, 
            detail="A senha deve ter no mínimo 6 caracteres, incluindo pelo menos uma letra maiúscula e uma minúscula" )
    
    if user.role_id is None:
        user.role_id = 1  # Atribui o papel padrão "Usuário" se nenhum papel for fornecido

    hashed_pw = hash_password(user.password)
    new_user = User(
        name=user.name,
        email=user.email,
        password=hashed_pw,
        role_id=user.role_id
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user