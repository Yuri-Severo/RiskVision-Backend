from passlib.context import CryptContext
import re

pwd_context = CryptContext(schemes=["argon2"])

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def validate_password(password: str) -> bool:
    pattern = r"^(?=.*[a-z])(?=.*[A-Z]).{6,}$"
    return bool(re.match(pattern, password))
