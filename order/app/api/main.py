from fastapi import APIRouter

from app.api.routes import health, order, order_history, order_item, shipping_details

api_router = APIRouter()

api_router.include_router(health.router, prefix="/health", tags=["health"])
api_router.include_router(order.router, prefix="/order", tags=["order"])
api_router.include_router(order_history.router, prefix="/order-history", tags=["order-history"])
api_router.include_router(order_item.router, prefix="/order-item", tags=["order-item"])
api_router.include_router(shipping_details.router, prefix="/shipping-details", tags=["shipping-details"])
