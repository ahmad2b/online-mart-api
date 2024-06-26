import asyncio
from contextlib import asynccontextmanager
from typing import AsyncGenerator
from fastapi import FastAPI

from app.core.db import create_db_and_tables
from app.api.main import api_router
from app.core.config import settings


@asynccontextmanager
async def lifespan(app: FastAPI)-> AsyncGenerator[None, None]:
    print("Creating tables..")
    create_db_and_tables()

    try:
        yield
    finally:
        print("Stopping app..")


app = FastAPI(
    lifespan=lifespan, 
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    version="0.0.1",
    )

@app.get("/")
def root():
    return {"message": "Hello World"}

app.include_router(api_router, prefix=settings.API_V1_STR)