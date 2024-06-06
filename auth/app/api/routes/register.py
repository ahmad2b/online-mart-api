from fastapi import APIRouter, HTTPException
from app import crud

from app.models import AuthUser, AuthUserCreate
from app.api.deps import SessionDep
from app.kafka.producer.auth_producer import AuthProducer
from app.core.config import settings

router = APIRouter()

@router.post("/register", response_model=AuthUser)
async def register_user(user_in: AuthUserCreate, session: SessionDep) -> AuthUser:
    user = crud.get_user_by_email(session=session, email=user_in.email)
    if user:
        raise HTTPException(status_code=400, detail="Email already registered")
    new_user = crud.create_user(session=session, user_create=user_in)
    # Produce Kafka event
    producer = AuthProducer(settings.BOOTSTRAP_SERVER)
    await producer.start()
    await producer.register_user(user_in.dict())
    await producer.stop()
    return new_user
