from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
from models.userModel import User
from schemas.userSchema import UserResponse
from schemas.userSchema import (
    UserResponse,
    RecoverPasswordRequest,
    UserCreate,
    UserBase,
)
from utils.security import hash_password, validate_password, verify_password

router = APIRouter(prefix="/users", tags=["Users"])

@router.get("/", response_model=list[UserResponse])
def get_users(db: Session = Depends(get_db)):
    return db.query(User).all()

@router.put("/recover-password")
def recover_password(request: RecoverPasswordRequest, db: Session = Depends(get_db)):

    user = db.query(User).filter(User.email == request.email).first()

    if not user:
        raise HTTPException(
            status_code=404, detail="O Email fornecido não está cadastrado"
        )

    if not validate_password(request.new_password):
        raise HTTPException(
            status_code=400,
            detail="A nova senha deve ter no mínimo 6 caracteres, incluindo pelo menos uma letra maiúscula e uma minúscula",
        )
    if verify_password(request.new_password, user.password):
        raise HTTPException(
            status_code=400,
            detail="A nova senha deve ser diferente da senha atual",
        )

    user.password = hash_password(request.new_password)
    db.commit()
    db.refresh(user)

    return {
        "message": "Sua senha foi atualizada com sucesso!",
        "user": {
            "name": user.name,
            "email": user.email,
        },
    }


@router.put("/{user_id}", response_model=UserResponse)
def update_user(user_id: int, user_data: UserBase, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    user.name = user_data.name
    user.email = user_data.email
    user.role_id = user_data.role_id
    db.commit()
    db.refresh(user)
    return user


@router.delete("/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    db.delete(user)
    db.commit()
    return {"message": "Usuário deletado com sucesso."}
