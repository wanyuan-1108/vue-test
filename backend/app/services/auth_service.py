from sqlalchemy.orm import Session

from app.core.config import get_settings
from app.core.security import create_access_token, hash_password, verify_password
from app.db.models import User


def build_auth_response(user: User) -> dict:
    settings = get_settings()
    access_token = create_access_token(
        subject=user.id,
        secret_key=settings.jwt_secret_key,
        algorithm=settings.jwt_algorithm,
        expire_minutes=settings.jwt_expire_minutes,
    )
    return {
        "user": user,
        "access_token": access_token,
        "token_type": "bearer",
    }


def register_user(db: Session, *, name: str, email: str, password: str) -> User:
    normalized_name = name.strip()
    normalized_email = email.strip().lower()
    existing_email_user = db.query(User).filter(User.email == normalized_email).first()
    if existing_email_user:
        raise ValueError("该邮箱已注册，请直接登录。")

    existing_name_user = db.query(User).filter(User.name == normalized_name).first()
    if existing_name_user:
        raise ValueError("该用户名已注册，请换一个用户名。")

    user = User(
        name=normalized_name,
        email=normalized_email,
        password_hash=hash_password(password),
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def authenticate_user(db: Session, *, email: str, password: str) -> User:
    normalized_email = email.strip().lower()
    user = db.query(User).filter(User.email == normalized_email).first()
    if user is None:
        raise ValueError("该邮箱尚未注册，请先注册账号。")
    if not verify_password(password, user.password_hash):
        raise ValueError("密码错误，请重新输入。")
    return user
