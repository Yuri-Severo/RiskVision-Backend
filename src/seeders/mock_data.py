import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from sqlalchemy.orm import Session
from database import get_db, Base, engine
from models.userModel import User
from schemas.userSchema import UserRole
from utils.security import hash_password

Base.metadata.create_all(bind=engine)

def seed_users(db: Session):
    users = [
        {"name": "Admin Teste", "email": "admin@test.com", "password": "Admin123!", "role": UserRole.ADMIN},
        {"name": "User Teste", "email": "user@test.com", "password": "User123!", "role": UserRole.USER}
    ]
    for u in users:
        existing_user = db.query(User).filter_by(email=u["email"]).first()
        if not existing_user:
            hashed_pw = hash_password(u["password"])
            new_user = User(name=u["name"], email=u["email"], password=hashed_pw, role=u["role"])
            db.add(new_user)
    db.commit()
    print("✅ Users seed executados.")

def main():
    db = next(get_db())
    try:
        seed_users(db)
    finally:
        db.close()

if __name__ == "__main__":
    main()
