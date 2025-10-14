from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from database import get_db
from models.userModel import User
from utils.jwtHandler import verify_access_token

security = HTTPBearer()

def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
) -> User:
    """
    Dependência para verificar o token JWT e retornar o usuário atual
    """
    try:
        # Extrair o token do header Authorization
        token = credentials.credentials
        
        # Decodificar o token
        payload = verify_access_token(token)
        if not payload:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token inválido ou expirado",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        # Extrair o user_id do payload (campo "sub" usado no login)
        user_id = payload.get("sub")
        if not user_id:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token inválido: user_id não encontrado",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        # Buscar o usuário no banco de dados
        user = db.query(User).filter(User.id == int(user_id)).first()
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Usuário não encontrado",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        return user
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Erro ao validar token",
            headers={"WWW-Authenticate": "Bearer"},
        )

def require_role(required_roles: list[str]):
    """
    Dependência para verificar se o usuário tem uma das roles necessárias
    """
    def role_checker(current_user: User = Depends(get_current_user)) -> User:
        if current_user.role not in required_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Acesso negado. Roles necessárias: {', '.join(required_roles)}"
            )
        return current_user
    
    return role_checker

# Dependências específicas para roles comuns
def require_admin(current_user: User = Depends(get_current_user)) -> User:
    """Requer role de administrador"""
    if current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Acesso negado. Role de administrador necessária"
        )
    return current_user

def require_user(current_user: User = Depends(get_current_user)) -> User:
    """Requer role de usuário comum"""
    if current_user.role != "user":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Acesso negado. Role de usuário necessária"
        )
    return current_user

def require_admin_or_user(current_user: User = Depends(get_current_user)) -> User:
    """Permite acesso para admin ou usuário comum"""
    if current_user.role not in ["admin", "user"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Acesso negado. Role válida necessária"
        )
    return current_user