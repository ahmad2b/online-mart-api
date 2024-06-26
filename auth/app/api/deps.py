from collections.abc import Generator
from typing import Annotated
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2AuthorizationCodeBearer
from jwt.exceptions import InvalidTokenError
from pydantic import ValidationError
from sqlmodel import Session
from fastapi import Depends, HTTPException, status

from app.core.db import engine
from app.core.config import settings
from app.models import AuthUser, TokenPayload
from app.core import security
import jwt

reusable_oauth2 = OAuth2PasswordBearer(
    tokenUrl=f"{settings.API_V1_STR}/login/access-token"
)

def get_db() -> Generator[Session, None, None]:
    with Session(engine) as session:
        yield session
        
SessionDep = Annotated[Session, Depends(get_db)]
TokenDep = Annotated[str, Depends(reusable_oauth2)]

def get_current_user(session: SessionDep, token: TokenDep) -> AuthUser:
    try:
        payload = jwt.decode(
            token, settings.PUBLIC_KEY, algorithms=[security.ALGORITHM]
        )
        token_data = TokenPayload(**payload)
    except (InvalidTokenError, ValidationError):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials",
        )
    user = session.get(AuthUser, token_data.sub)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    if not user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    return user

CurrentUser = Annotated[AuthUser, Depends(get_current_user)]

def get_current_active_superuser(current_user: CurrentUser) -> AuthUser:
    if not current_user.is_superuser:
        raise HTTPException(
            status_code=403, detail="The user doesn't have enough privileges"
        )
    return current_user