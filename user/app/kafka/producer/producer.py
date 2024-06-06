import asyncio
import json
from aiokafka import AIOKafkaProducer
from fastapi import Depends
from app.core.config import settings

from app.core import security


async def get_kafka_producer():
    producer = AIOKafkaProducer(bootstrap_servers=settings.BOOTSTRAP_SERVER)
    await producer.start()
    try:
        yield producer
    finally:
        await producer.stop()

async def produce_message(producer: AIOKafkaProducer, topic: str, message: dict):
    await producer.send_and_wait(topic, json.dumps(message).encode("utf-8"))

class BaseProducer:
    def __init__(self, bootstrap_servers):
        self.producer = AIOKafkaProducer(bootstrap_servers=bootstrap_servers)

    async def start(self):
        await self.producer.start()

    async def stop(self):
        await self.producer.stop()

    async def send(self, topic, message):
        await self.producer.send_and_wait(topic, json.dumps(message).encode('utf-8'))
        
class OrderProducer(BaseProducer):
    def __init__(self, bootstrap_servers):
        super().__init__(bootstrap_servers)

    async def produce_order_created(self, order_data):
        await self.send('order_created', order_data)

    async def produce_order_updated(self, order_data):
        await self.send('order_updated', order_data)
        
from aiokafka import AIOKafkaProducer
import json

class AuthService(BaseProducer):
    def __init__(self, bootstrap_servers):
        super().__init__(bootstrap_servers)

    async def register_user(self, user_data):
        await self.send("auth_events", user_data)

    async def login_user(self, login_data):
        # Handle user login logic
        token = security.create_access_token(login_data)
        data = {
            "user": login_data,
            "token": token
        }
        await self.send("auth_events", data)
        return token


        

async def get_order_producer():
    producer = OrderProducer(settings.BOOTSTRAP_SERVER)
    await producer.start()
    try:
        yield producer
    finally:
        await producer.stop()