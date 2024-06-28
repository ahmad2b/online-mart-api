from fastapi import APIRouter

from app.api.routes import health, inventory, adjustments, reservations

api_router = APIRouter()
api_router.include_router(health.router, prefix="/health", tags=["health"])
api_router.include_router(inventory.router, prefix="/inventory", tags=["inventory"])
api_router.include_router(adjustments.router, prefix="/adjustments", tags=["adjustments"])
api_router.include_router(reservations.router, prefix="/reservations", tags=["reservations"])