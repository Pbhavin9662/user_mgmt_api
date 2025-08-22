from sqlalchemy.orm import Session
from sqlalchemy import select, func
from typing import Optional, Tuple

from app.models.user import User
from app.core.security import hash_password, verify_password

def get_by_email(db: Session, email: str) -> Optional[User]:
    return db.execute(select(User).where(User.email == email)).scalar_one_or_none()

def create_user(db: Session, name: str, email: str, password: str, role: str = "user") -> User:
    user = User(name=name, email=email, password_hash=hash_password(password), role=role)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

def authenticate(db: Session, email: str, password: str) -> Optional[User]:
    user = get_by_email(db, email)
    if not user:
        return None
    if not verify_password(password, user.password_hash):
        return None
    return user

def get_by_id(db: Session, user_id: str) -> Optional[User]:
    return db.get(User, user_id)

def list_users(db: Session, page: int, limit: int) -> Tuple[list[User], int]:
    total = db.execute(select(func.count()).select_from(User)).scalar_one()
    items = db.execute(select(User).order_by(User.created_at.desc()).offset((page-1)*limit).limit(limit)).scalars().all()
    return items, total
