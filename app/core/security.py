from datetime import datetime, timedelta, timezone
from typing import Optional
import hashlib
from jose import jwt
from app.core.config import settings

ALGORITHM = "HS256"

# --------------------
# JWT Token functions
# --------------------
def create_access_token(subject: str, expires_minutes: Optional[int] = None) -> str:
    if expires_minutes is None:
        expires_minutes = settings.access_token_expires_min
    expire = datetime.now(tz=timezone.utc) + timedelta(minutes=expires_minutes)
    to_encode = {"sub": subject, "exp": expire}
    token = jwt.encode(to_encode, settings.jwt_secret, algorithm=ALGORITHM)
    return token

def decode_access_token(token: str) -> dict:
    try:
        payload = jwt.decode(token, settings.jwt_secret, algorithms=[ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        raise Exception("Token expired")
    except jwt.JWTError:
        raise Exception("Invalid token")

# --------------------
# Password functions
# --------------------
def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return hash_password(plain_password) == hashed_password
