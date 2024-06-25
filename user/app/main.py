import asyncio
from contextlib import asynccontextmanager
from typing import AsyncGenerator
from fastapi import FastAPI

from app.core.db import create_db_and_tables
from app.api.main import api_router
from app.core.config import settings
from app.kafka.consumer.index import UserConsumer


@asynccontextmanager
async def lifespan(app: FastAPI)-> AsyncGenerator[None, None]:
    print("Creating tables..")
    create_db_and_tables()
    consumer = UserConsumer(
        settings.BOOTSTRAP_SERVER, 
        settings.KAFKA_CONSUMER_GROUP_ID
    )
    await (consumer.start())
    asyncio.create_task(consumer.consume())
    
    try:
        yield
    finally:
        print("Stopping consumer..")
        # await consumer.stop()
        # task.cancel()
        # await task
        # print("Consumer stopped..")
        # print("Closing tables..")
        # await close_db_and_tables()
        # print("Tables closed..")
        # print("App stopped..") 

app = FastAPI(
    lifespan=lifespan, 
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    version="0.0.1",
    )

@app.get("/")
def read_root():
    return {"Hello": "User Service"}

app.include_router(api_router, prefix=settings.API_V1_STR)