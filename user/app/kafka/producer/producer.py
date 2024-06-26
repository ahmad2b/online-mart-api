import json
from aiokafka import AIOKafkaProducer
from fastapi import Depends
from app.core.config import settings

class UserProducer:
    def __init__(self, bootstrap_servers=settings.BOOTSTRAP_SERVER):
        self.producer = AIOKafkaProducer(bootstrap_servers=bootstrap_servers)

    async def start(self):
        await self.producer.start()

    async def stop(self):
        await self.producer.stop()

    async def send(self, topic, message):
        await self.producer.send_and_wait(topic, json.dumps(message).encode('utf-8'))

    async def user_created(self, user_data):
        await self.send("user_registered", {"type": "user_registered", "data": user_data})

    async def user_updated(self, user_data):
        await self.send("user_updated", {"type": "user_updated", "data": user_data})

    async def user_deleted(self, user_data):
        await self.send("user_deleted", {"type": "user_deleted", "data": user_data})

# Dependency for FastAPI
async def get_user_producer():
    producer = UserProducer()
    await producer.start()
    try:
        yield producer
    finally:
        await producer.stop()
