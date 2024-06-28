from fastapi import APIRouter

from app.api.routes import health, cart, cart_item

api_router = APIRouter()
api_router.include_router(health.router, prefix="/health", tags=["health"])
api_router.include_router(cart.router, prefix="/carts", tags=["carts"])
api_router.include_router(cart_item.router, prefix="/carts", tags=["cart_items"])
