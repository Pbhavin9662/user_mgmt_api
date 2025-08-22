from fastapi import APIRouter, Depends, HTTPException, status, Query
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.core.config import settings
from app.schemas.user import UserCreate, UserOut, UsersListResponse
from app.services.user_service import get_by_email, create_user, get_by_id, list_users

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

router = APIRouter()

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    try:
        payload = jwt.decode(token, settings.jwt_secret, algorithms=["HS256"])
        user_id: str = payload.get("sub")
        if user_id is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")

    user = get_by_id(db, user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")
    return user

def require_admin(user=Depends(get_current_user)):
    if user.role != "admin":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Admins only")
    return user

@router.post("/users", response_model=UserOut, status_code=status.HTTP_201_CREATED)
def register(payload: UserCreate, db: Session = Depends(get_db)):
    if get_by_email(db, payload.email):
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Email already registered")
    user = create_user(db, name=payload.name, email=payload.email, password=payload.password)
    return UserOut(id=user.id, name=user.name, email=user.email, role=user.role)

@router.get("/me", response_model=UserOut)
def me(current_user = Depends(get_current_user)):
    return UserOut(id=current_user.id, name=current_user.name, email=current_user.email, role=current_user.role)

@router.get("/users/{user_id}", response_model=UserOut)
def get_user_by_id(user_id: str, current_user = Depends(get_current_user), db: Session = Depends(get_db)):
    if current_user.role != "admin" and current_user.id != user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")
    user = get_by_id(db, user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return UserOut(id=user.id, name=user.name, email=user.email, role=user.role)

@router.get("/users", response_model=UsersListResponse, dependencies=[Depends(require_admin)])
def list_users_endpoint(
    page: int = Query(default=1, ge=1),
    limit: int = Query(default=20, ge=1, le=100),
    db: Session = Depends(get_db)
):
    items, total = list_users(db, page=page, limit=limit)
    data = [UserOut(id=u.id, name=u.name, email=u.email, role=u.role) for u in items]
    return UsersListResponse(data=data, page=page, limit=limit, total=total)
