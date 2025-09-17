from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
from models.roleModel import Role
from schemas.roleSchema import RoleCreate, RoleResponse

router = APIRouter(prefix="/roles", tags=["Roles"])

@router.get("/", response_model=list[RoleResponse])
def get_roles(db: Session = Depends(get_db)):
    return db.query(Role).all()

@router.post("/", response_model=RoleResponse)
def create_role(role: RoleCreate, db: Session = Depends(get_db)):
    new_role = Role(description=role.description)
    db.add(new_role)
    db.commit()
    db.refresh(new_role)
    return new_role
