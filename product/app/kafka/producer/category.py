import json
from aiokafka import AIOKafkaProducer
from fastapi import Depends
from app.core.config import settings

class CategoryProducer:
    def __init__(self, bootstrap_servers=settings.BOOTSTRAP_SERVER):
        self.producer = AIOKafkaProducer(bootstrap_servers=bootstrap_servers)

    async def start(self):
        await self.producer.start()

    async def stop(self):
        await self.producer.stop()

    async def send(self, topic, message):
        await self.producer.send_and_wait(topic, json.dumps(message).encode('utf-8'))

    async def category_created(self, category_data):
        await self.send("category_created", {"type": "category_created", "data": category_data})

    async def category_updated(self, category_data):
        await self.send("category_updated", {"type": "category_updated", "data": category_data})

    async def category_deleted(self, category_data):
        await self.send("category_deleted", {"type": "category_deleted", "data": category_data})

# Dependency for FastAPI
async def get_category_producer():
    producer = CategoryProducer()
    await producer.start()
    try:
        yield producer
    finally:
        await producer.stop()
