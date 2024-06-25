import asyncio
from contextlib import asynccontextmanager
from typing import AsyncGenerator
from fastapi import FastAPI

from app.core.db import create_db_and_tables
from app.api.main import api_router
from app.core.config import settings

from app.kafka.consumer.product import ProductConsumer
from app.kafka.consumer.category import CategoryConsumer
from app.kafka.consumer.brand import BrandConsumer


@asynccontextmanager
async def lifespan(app: FastAPI)-> AsyncGenerator[None, None]:
    print("Creating tables..")
    create_db_and_tables()
    
    product_consumer = ProductConsumer(bootstrap_servers=settings.BOOTSTRAP_SERVER, group_id="product_group")
    category_consumer = CategoryConsumer(bootstrap_servers=settings.BOOTSTRAP_SERVER, group_id="category_group")
    brand_consumer = BrandConsumer(bootstrap_servers=settings.BOOTSTRAP_SERVER, group_id="brand_group")
    
    await product_consumer.start()
    await category_consumer.start()
    await brand_consumer.start()

    product_task = asyncio.create_task(product_consumer.consume())
    category_task = asyncio.create_task(category_consumer.consume())
    brand_task = asyncio.create_task(brand_consumer.consume())
    
    try:
        yield
    finally:
        print("Stopping consumers...")
        await product_consumer.stop()
        await category_consumer.stop()
        await brand_consumer.stop()
        product_task.cancel()
        category_task.cancel()
        brand_task.cancel()
        print("Consumers stopped.")
        # await close_db_and_tables()
        # print("Tables closed..")
        # print("App stopped..") 

app = FastAPI(
    lifespan=lifespan, 
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    version="0.0.1",
    )

app.include_router(api_router, prefix=settings.API_V1_STR)