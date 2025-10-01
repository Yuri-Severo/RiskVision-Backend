from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
from models.userModel import User
from schemas.userSchema import UserResponse

router = APIRouter(prefix="/users", tags=["Users"])

@router.get("/", response_model=list[UserResponse])
def get_users(db: Session = Depends(get_db)):
    return db.query(User).all()
