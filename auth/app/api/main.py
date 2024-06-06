from fastapi import APIRouter

from app.api.routes import login, register, password_reset

api_router = APIRouter()
api_router.include_router(login.router, tags=["login"])
api_router.include_router(register.router, tags=["register"])
api_router.include_router(password_reset.router, tags=["password-reset"])