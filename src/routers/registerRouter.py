from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models.userModel import User
from schemas.userSchema import UserCreate, UserResponse
from utils.security import hash_password, validate_password

router = APIRouter(prefix="/register", tags=["Register"])

@router.post("/", response_model=UserResponse)
def register_user(user: UserCreate, db: Session = Depends(get_db)):
    existing_user = db.query(User).filter(User.email == user.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email já cadastrado")

    if not validate_password(user.password):
        raise HTTPException(
            status_code=400,
            detail="A senha deve ter no mínimo 6 caracteres, incluindo pelo menos uma letra maiúscula e uma minúscula",
        )
    #Caso o role_id não seja fornecido, atribui o papel padrão "Usuário" (id=2)
    if user.role_id is None:
        user.role_id = 2

    hashed_pw = hash_password(user.password)
    new_user = User(
        name=user.name, email=user.email, password=hashed_pw, role_id=user.role_id
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user
