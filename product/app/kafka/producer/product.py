import json
from aiokafka import AIOKafkaProducer
from app.core.config import settings

class ProductProducer:
    def __init__(self, bootstrap_servers=settings.BOOTSTRAP_SERVER):
        self.producer = AIOKafkaProducer(bootstrap_servers=bootstrap_servers)

    async def start(self):
        await self.producer.start()

    async def stop(self):
        await self.producer.stop()

    async def send(self, topic, message):
        await self.producer.send_and_wait(topic, json.dumps(message).encode('utf-8'))

    async def product_created(self, product_data):
        await self.send("product_created", {"type": "product_created", "data": product_data})

    async def product_updated(self, product_data):
        await self.send("product_updated", {"type": "product_updated", "data": product_data})

    async def product_deleted(self, product_data):
        await self.send("product_deleted", {"type": "product_deleted", "data": product_data})

# Dependency for FastAPI
async def get_product_producer():
    producer = ProductProducer()
    await producer.start()
    try:
        yield producer
    finally:
        await producer.stop()
