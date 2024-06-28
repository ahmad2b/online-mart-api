import json
from aiokafka import AIOKafkaProducer
from app.core.config import settings

class CartItemProducer:
    def __init__(self, bootstrap_servers=settings.BOOTSTRAP_SERVER):
        self.producer = AIOKafkaProducer(bootstrap_servers=bootstrap_servers)

    async def start(self):
        await self.producer.start()

    async def stop(self):
        await self.producer.stop()

    async def send(self, topic, message):
        await self.producer.send_and_wait(topic, json.dumps(message).encode('utf-8'))
        
    async def cart_item_created(self, cart_item_data):
        await self.send("cart_item_created", {"type": "cart_item_created", "data": cart_item_data})

    async def cart_item_updated(self, cart_item_data):
        await self.send("cart_item_updated", {"type": "cart_item_updated", "data": cart_item_data})

    async def cart_item_deleted(self, cart_item_data):
        await self.send("cart_item_deleted", {"type": "cart_item_deleted", "data": cart_item_data})

# Dependency for FastAPI
async def get_cart_item_producer():
    producer = CartItemProducer()
    await producer.start()
    try:
        yield producer
    finally:
        await producer.stop()
