from fastapi import APIRouter, Depends, HTTPException, status, Request
from fastapi.security import OAuth2PasswordRequestForm
from slowapi import Limiter
from slowapi.util import get_remote_address

from sqlalchemy.orm import Session

from app.schemas.user import TokenResponse
from app.services.user_service import authenticate
from app.core.security import create_access_token
from app.db.session import get_db
from app.core.config import settings

limiter = Limiter(key_func=get_remote_address)

router = APIRouter()

@router.post("/login", response_model=TokenResponse)
@limiter.limit("5/minute")
def login(request: Request, form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = authenticate(db, email=form_data.username, password=form_data.password)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    token = create_access_token(subject=user.id, expires_minutes=settings.access_token_expires_min)
    return TokenResponse(access_token=token, expires_in=settings.access_token_expires_min)
