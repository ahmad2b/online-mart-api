from fastapi import APIRouter, Depends, HTTPException
from jose import JWTError, jwt
from pydantic import ValidationError
from app.models import TokenPayload, AuthUser, AuthUserPublic
from app.core.config import settings
from app.core.security import ALGORITHM
from app.api.deps import SessionDep
from sqlmodel import select, SQLModel

class TokenData(SQLModel):
    token: str

router = APIRouter()

@router.post("/verify-token", response_model=AuthUserPublic)
async def verify_token(token_data: TokenData, session: SessionDep) -> AuthUserPublic:
    try:
        token = token_data.token
        payload = jwt.decode(token, settings.PRIVATE_KEY, algorithms=[ALGORITHM])
        token_data = TokenPayload(**payload)
    except (JWTError, ValidationError):
        raise HTTPException(
            status_code=403,
            detail="Could not validate credentials",
        )
    user = await get_user_by_id(token_data.sub, session) 
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    if not user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    # Convert AuthUser to AuthUserPublic
    user_public = AuthUserPublic(id=user.id, email=user.email, full_name=user.full_name, is_active=user.is_active, is_superuser=user.is_superuser)
    return user_public
async def get_user_by_id(user_id: int, session: SessionDep) -> AuthUser:
    statement = select(AuthUser).where(AuthUser.id == user_id)
    return session.exec(statement).first()
