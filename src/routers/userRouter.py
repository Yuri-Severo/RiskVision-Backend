from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database import get_db
from models.userModel import User
from schemas.userSchema import UserResponse, RecoverPasswordRequest, UserCreate, UserBase, UserRole
from utils.security import hash_password, validate_password, verify_password
from routers.authRouter import get_current_user  

router = APIRouter(prefix="/users", tags=["Users"])

def get_current_admin(current_user: User = Depends(get_current_user)):
    if current_user.role != UserRole.ADMIN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Acesso negado. Apenas administradores podem realizar esta operação."
        )
    return current_user



@router.get("/", response_model=list[UserResponse])
def get_users(
    current_admin: User = Depends(get_current_admin),  
    db: Session = Depends(get_db)
):
    return db.query(User).all()


@router.get("/me", response_model=UserResponse)
def get_current_user_info(current_user: User = Depends(get_current_user)):
    return current_user


@router.put("/recover-password")
def recover_password(
    request: RecoverPasswordRequest,
    current_user: User = Depends(get_current_user), 
    db: Session = Depends(get_db)):

    
    # Verifica se o email corresponde ao usuário logado
    if current_user.email != request.email:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Você só pode alterar sua própria senha"
        )

    if not validate_password(request.new_password):
        raise HTTPException(
            status_code=400,
            detail="A nova senha deve ter no mínimo 6 caracteres, incluindo pelo menos uma letra maiúscula e uma minúscula",
        )
    
    if verify_password(request.new_password, current_user.password):
        raise HTTPException(
            status_code=400,
            detail="A nova senha deve ser diferente da senha atual",
        )

    current_user.password = hash_password(request.new_password)
    db.commit()
    db.refresh(current_user)

    return {
        "message": "Sua senha foi atualizada com sucesso!",
        "user": {
            "name": current_user.name,
            "email": current_user.email,
        },
    }


@router.put("/{user_id}", response_model=UserResponse)
def update_user(
    user_id: int,
    user_data: UserBase,
    current_admin: User = Depends(get_current_admin),  
    db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    
    if not user:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    
    user.name = user_data.name
    user.email = user_data.email
    user.role = user_data.role
    
    db.commit()
    db.refresh(user)
    
    return user


@router.delete("/{user_id}")
def delete_user(
    user_id: int,
    current_admin: User = Depends(get_current_admin),  
    db: Session = Depends(get_db)
):
    
    
    # Impede que o admin se deletee
    if current_admin.id == user_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Você não pode deletar sua própria conta"
        )
    
    user = db.query(User).filter(User.id == user_id).first()
    
    if not user:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    
    db.delete(user)
    db.commit()
    
    return {"message": "Usuário deletado com sucesso."}