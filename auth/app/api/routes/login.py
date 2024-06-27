from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm 

from app import crud
from app.core.security import create_access_token
from app.api.deps import SessionDep
from app.models import Token
from app.core.config import settings
from app.kafka.producer.auth_producer import AuthProducer

router = APIRouter()

@router.post("/login/access-token", response_model=Token)
async def login_access_token(session: SessionDep, form_data: OAuth2PasswordRequestForm = Depends(), ) -> Token:
    user = crud.authenticate_user(session=session, email=form_data.username, password=form_data.password)
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect email or password")
    elif not user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    token = create_access_token(user.id, user.full_name, user.email, expires_delta=access_token_expires)
    # Produce Kafka event
    producer = AuthProducer(settings.BOOTSTRAP_SERVER)
    await producer.start()
    await producer.login_user({"email": user.email, "token": token})
    await producer.stop()
    return Token(access_token=token, token_type="bearer")
