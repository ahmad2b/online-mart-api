import asyncio
from contextlib import asynccontextmanager
from typing import AsyncGenerator
from fastapi import FastAPI

from app.core.db import create_db_and_tables
from app.api.main import api_router
from app.core.config import settings

from app.kafka.consumer.inventory import InventoryConsumer
from app.kafka.consumer.reservation import ReservationConsumer
from app.kafka.consumer.adjustment import AdjustmentConsumer


@asynccontextmanager
async def lifespan(app: FastAPI)-> AsyncGenerator[None, None]:
    print("Creating tables..")
    create_db_and_tables()
    
    inventory_consumer = InventoryConsumer(bootstrap_servers=settings.BOOTSTRAP_SERVER, group_id="inventory_group")
    reservation_consumer = ReservationConsumer(bootstrap_servers=settings.BOOTSTRAP_SERVER, group_id="reservation_group")
    adjustment_consumer = AdjustmentConsumer(bootstrap_servers=settings.BOOTSTRAP_SERVER, group_id="adjustment_group")
    
    await inventory_consumer.start()
    await reservation_consumer.start()
    await adjustment_consumer.start()
    
    inventory_task = asyncio.create_task(inventory_consumer.consume())
    reservation_task = asyncio.create_task(reservation_consumer.consume())
    adjustment_task = asyncio.create_task(adjustment_consumer.consume())

    try:
        yield
    finally:
        print("Stopping consumers...")
        await inventory_consumer.stop()
        await reservation_consumer.stop()
        await adjustment_consumer.stop()
        inventory_task.cancel()
        reservation_task.cancel()
        adjustment_task.cancel()
        print("Consumers stopped.")
        
        print("Stopping app..")


app = FastAPI(
    lifespan=lifespan, 
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    version="0.0.1",
    )

app.include_router(api_router, prefix=settings.API_V1_STR)