import json
from aiokafka import AIOKafkaProducer
from fastapi import Depends
from app.core.config import settings

class BrandProducer:
    def __init__(self, bootstrap_servers=settings.BOOTSTRAP_SERVER):
        self.producer = AIOKafkaProducer(bootstrap_servers=bootstrap_servers)

    async def start(self):
        await self.producer.start()

    async def stop(self):
        await self.producer.stop()

    async def send(self, topic, message):
        await self.producer.send_and_wait(topic, json.dumps(message).encode('utf-8'))

    async def brand_created(self, brand_data):
        await self.send("brand_created", {"type": "brand_created", "data": brand_data})

    async def brand_updated(self, brand_data):
        await self.send("brand_updated", {"type": "brand_updated", "data": brand_data})

    async def brand_deleted(self, brand_data):
        await self.send("brand_deleted", {"type": "brand_deleted", "data": brand_data})

# Dependency for FastAPI
async def get_brand_producer():
    producer = BrandProducer()
    await producer.start()
    try:
        yield producer
    finally:
        await producer.stop()
