from typing import Any

from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select, func
from app import crud
from app.api.deps import CurrentUser, SessionDep, get_current_active_superuser
from app.core.config import settings
from app.models import (
    Message, User, UserCreate, UserPublic, UserUpdate, UserUpdateMe, UsersPublic
)
from app.kafka.producer.producer import UserProducer
from app.utils import generate_new_account_email, send_email

router = APIRouter(prefix="/users", tags=["users"])

@router.get("/", dependencies=[Depends(get_current_active_superuser)], response_model=UsersPublic)
def read_users(session: SessionDep, skip: int = 0, limit: int = 100) -> Any:
    """
    Retrieve users.
    """
    count_statement = select(func.count()).select_from(User)
    count = session.exec(count_statement).one()

    statement = select(User).offset(skip).limit(limit)
    users = session.exec(statement).all()

    return UsersPublic(data=users, count=count)

@router.post("/", dependencies=[Depends(get_current_active_superuser)], response_model=UserPublic)
async def create_user(*, session: SessionDep, user_in: UserCreate, producer: UserProducer = Depends()) -> Any:
    """
    Create new user.
    """
    user = crud.get_user_by_email(session=session, email=user_in.email)
    if user:
        raise HTTPException(status_code=400, detail="The user with this email already exists in the system.")

    user = crud.create_user(session=session, user_create=user_in)
    await producer.user_created(user.dict())
    if settings.emails_enabled and user_in.email:
        email_data = generate_new_account_email(email_to=user_in.email, username=user_in.email)
        send_email(email_to=user_in.email, subject=email_data.subject, html_content=email_data.html_content)
    return user

@router.patch("/me", response_model=UserPublic)
async def update_user_me(*, session: SessionDep, user_in: UserUpdateMe, current_user: CurrentUser, producer: UserProducer = Depends()) -> Any:
    """
    Update own user.
    """
    if user_in.email:
        existing_user = crud.get_user_by_email(session=session, email=user_in.email)
        if existing_user and existing_user.id != current_user.id:
            raise HTTPException(status_code=409, detail="User with this email already exists")
    
    user_data = user_in.model_dump(exclude_unset=True)
    current_user.sqlmodel_update(user_data)
    session.add(current_user)
    session.commit()
    session.refresh(current_user)
    await producer.user_updated(current_user.dict())
    return current_user

@router.get("/me", response_model=UserPublic)
def read_user_me(current_user: CurrentUser) -> Any:
    """
    Get current user.
    """
    return current_user

@router.delete("/me", response_model=Message)
async def delete_user_me(session: SessionDep, current_user: CurrentUser, producer: UserProducer = Depends()) -> Any:
    """
    Delete own user.
    """
    if current_user.is_superuser:
        raise HTTPException(status_code=403, detail="Super users are not allowed to delete themselves")
    
    session.delete(current_user)
    session.commit()
    await producer.user_deleted(current_user.dict())
    return Message(message="User deleted successfully")

@router.post("/signup", response_model=UserPublic)
async def register_user(session: SessionDep, user_in: UserCreate, producer: UserProducer = Depends()) -> Any:
    """
    Create new user without the need to be logged in.
    """
    if not settings.USERS_OPEN_REGISTRATION:
        raise HTTPException(status_code=403, detail="Open user registration is forbidden on this server")
    
    user = crud.get_user_by_email(session=session, email=user_in.email)
    if user:
        raise HTTPException(status_code=400, detail="The user with this email already exists in the system")
    
    user = crud.create_user(session=session, user_create=user_in)
    await producer.user_created(user.dict())
    return user

@router.get("/{user_id}", response_model=UserPublic)
def read_user_by_id(user_id: int, session: SessionDep, current_user: CurrentUser) -> Any:
    """
    Get a specific user by id.
    """
    user = session.get(User, user_id)
    if user == current_user:
        return user
    if not current_user.is_superuser:
        raise HTTPException(status_code=403, detail="The user doesn't have enough privileges")
    return user

@router.patch("/{user_id}", dependencies=[Depends(get_current_active_superuser)], response_model=UserPublic)
async def update_user(*, session: SessionDep, user_id: int, user_in: UserUpdate, producer: UserProducer = Depends()) -> Any:
    """
    Update a user.
    """
    db_user = session.get(User, user_id)
    if not db_user:
        raise HTTPException(status_code=404, detail="The user with this id does not exist in the system")
    
    if user_in.email:
        existing_user = crud.get_user_by_email(session=session, email=user_in.email)
        if existing_user and existing_user.id != user_id:
            raise HTTPException(status_code=409, detail="User with this email already exists")
    
    db_user = crud.update_user(session=session, db_user=db_user, user_in=user_in)
    await producer.user_updated(db_user.dict())
    return db_user

@router.delete("/{user_id}", dependencies=[Depends(get_current_active_superuser)], response_model=Message)
async def delete_user(session: SessionDep, current_user: CurrentUser, user_id: int, producer: UserProducer = Depends()) -> Message:
    """
    Delete a user.
    """
    user = session.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    if user == current_user:
        raise HTTPException(status_code=403, detail="Super users are not allowed to delete themselves")
    
    session.delete(user)
    session.commit()
    await producer.user_deleted(user.dict())
    return Message(message="User deleted successfully")
