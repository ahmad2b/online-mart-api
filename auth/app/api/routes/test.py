# api/routes/test.py
from fastapi import APIRouter, Depends
from app.api.deps import SessionDep, get_current_user

router = APIRouter()

@router.get("/test-token", response_model=dict)
async def test_token(session: SessionDep, user: str = Depends(get_current_user)) -> dict:
    print(user)
    return {"message": "Token is valid", "user": user}