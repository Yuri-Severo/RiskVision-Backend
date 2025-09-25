import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from sqlalchemy.orm import Session
from database import get_db
from models.userModel import User
from models.roleModel import Role
from utils.security import hash_password

def seed_roles(db: Session):
    roles = [{"id": 1, "description": "Admin"}, {"id": 2, "description": "Usuário"}]
    for role_data in roles:
        role = db.query(Role).filter_by(id=role_data["id"]).first()
        if not role:
            new_role = Role(id=role_data["id"], description=role_data["description"])
            db.add(new_role)
    db.commit()
    print("✅ Roles seed executadas.")

def seed_users(db: Session):
    users = [
        {"name": "Admin Teste", "email": "admin@test.com", "password": "Admin123!", "role_id": 1},
        {"name": "User Teste", "email": "user@test.com", "password": "User123!", "role_id": 2}
    ]
    for u in users:
        existing_user = db.query(User).filter_by(email=u["email"]).first()
        if not existing_user:
            hashed_pw = hash_password(u["password"])
            new_user = User(name=u["name"], email=u["email"], password=hashed_pw, role_id=u["role_id"])
            db.add(new_user)
    db.commit()
    print("✅ Users seed executados.")

def main():
    db = next(get_db())
    try:
        seed_roles(db)
        seed_users(db)
    finally:
        db.close()

if __name__ == "__main__":
    main()
