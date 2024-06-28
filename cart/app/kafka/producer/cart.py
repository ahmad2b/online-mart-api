import json
from aiokafka import AIOKafkaProducer
from app.core.config import settings

class CartProducer:
    def __init__(self, bootstrap_servers=settings.BOOTSTRAP_SERVER):
        self.producer = AIOKafkaProducer(bootstrap_servers=bootstrap_servers)

    async def start(self):
        await self.producer.start()

    async def stop(self):
        await self.producer.stop()

    async def send(self, topic, message):
        await self.producer.send_and_wait(topic, json.dumps(message).encode('utf-8'))
        
    async def cart_created(self, cart_data):
        await self.send("cart_created", {"type": "cart_created", "data": cart_data})

    async def cart_updated(self, cart_data):
        await self.send("cart_updated", {"type": "cart_updated", "data": cart_data})

    async def cart_deleted(self, cart_data):
        await self.send("cart_deleted", {"type": "cart_deleted", "data": cart_data})

# Dependency for FastAPI
async def get_cart_producer():
    producer = CartProducer()
    await producer.start()
    try:
        yield producer
    finally:
        await producer.stop()
