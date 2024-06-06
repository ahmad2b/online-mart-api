import asyncio
from contextlib import asynccontextmanager
from typing import AsyncGenerator
from fastapi import FastAPI

from app.core.db import create_db_and_tables
from app.kafka.producer.producer import get_kafka_producer, produce_message
from app.kafka.consumer.consumer import consume_messages
from app.kafka.consumer.user_consumer import UserConsumer


from app.api.main import api_router
from app.core.config import settings


# auth_event_consumer = AuthEventConsumer(kafka_servers=["kafka:9092"])


@asynccontextmanager
async def lifespan(app: FastAPI)-> AsyncGenerator[None, None]:
    print("Creating tables..")
    create_db_and_tables()
    consumer = UserConsumer(settings.BOOTSTRAP_SERVER, settings.KAFKA_CONSUMER_GROUP_ID)
    asyncio.create_task(consumer.consume())


    # task = asyncio.create_task(consume_messages(
    #     topics=["users"],  # List the topics you want to consume
    #     bootstrap_servers=settings.BOOTSTRAP_SERVER,
    #     group_id=settings.KAFKA_CONSUMER_GROUP_ID
    # ))
    yield

app = FastAPI(
    lifespan=lifespan, 
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    version="0.0.1",
    )

# @app.on_event("")


@app.get("/")
def read_root():
    return {"Hello": "User Service"}


app.include_router(api_router, prefix=settings.API_V1_STR)