from fastapi import APIRouter

from app.api.routes import login, register, password_reset, test, verify

api_router = APIRouter()
api_router.include_router(login.router, tags=["login"])
api_router.include_router(register.router, tags=["register"])
api_router.include_router(password_reset.router, tags=["password-reset"])
api_router.include_router(test.router, tags=["test-token"])
api_router.include_router(verify.router, tags=["verify-token"])