from sqlmodel import Session, select
from app.models import AuthUser, AuthUserCreate
from app.core.security import get_password_hash, verify_password

def create_user(*, session: Session, user_create: AuthUserCreate) -> AuthUser:
    db_obj = AuthUser(
        email=user_create.email,
        full_name=user_create.full_name,
        hashed_password=get_password_hash(user_create.password),
        is_active=user_create.is_active,
        is_superuser=user_create.is_superuser
    )
    session.add(db_obj)
    session.commit()
    session.refresh(db_obj)
    return db_obj

def get_user_by_email(*, session: Session, email: str) -> AuthUser | None:
    statement = select(AuthUser).where(AuthUser.email == email)
    return session.exec(statement).first()

def authenticate_user(*, session: Session, email: str, password: str) -> AuthUser | None:
    user = get_user_by_email(session=session, email=email)
    if not user or not verify_password(password, user.hashed_password):
        return None
    return user
