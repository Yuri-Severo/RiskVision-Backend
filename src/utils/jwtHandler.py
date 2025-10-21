from datetime import datetime, timedelta
from jose import JWTError, jwt
import os
import uuid
from dotenv import load_dotenv

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY", "changeme")
ALGORITHM = os.getenv("ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30))


def _to_timestamp(dt: datetime) -> int:
    """Converte datetime UTC para timestamp inteiro (segundos)."""
    return int(dt.timestamp())


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    """
    Cria um JWT adicionando as claims padrão:
    - exp (timestamp em segundos)
    - iat (issued at, timestamp em segundos)
    - jti (identificador único do token)

    Isso torna o token único mesmo que o payload base seja igual.
    """
    to_encode = data.copy()
    now = datetime.utcnow()
    expire = now + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))

    to_encode.update({
        "exp": _to_timestamp(expire),
        "iat": _to_timestamp(now),
        "jti": str(uuid.uuid4()),
    })

    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def verify_access_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        return None
