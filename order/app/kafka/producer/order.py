import json
from aiokafka import AIOKafkaProducer
from app.core.config import settings

class OrderProducer:
    def __init__(self, bootstrap_servers=settings.BOOTSTRAP_SERVER):
        self.producer = AIOKafkaProducer(bootstrap_servers=bootstrap_servers)

    async def start(self):
        await self.producer.start()

    async def stop(self):
        await self.producer.stop()

    async def send(self, topic, message):
        await self.producer.send_and_wait(topic, json.dumps(message).encode('utf-8'))

    async def order_created(self, order_data):
        await self.send("order_created", {"type": "order_created", "data": order_data})

    async def order_updated(self, order_data):
        await self.send("order_updated", {"type": "order_updated", "data": order_data})

    async def order_deleted(self, order_data):
        await self.send("order_deleted", {"type": "order_deleted", "data": order_data})

# Dependency for FastAPI
async def get_order_producer():
    producer = OrderProducer()
    await producer.start()
    try:
        yield producer
    finally:
        await producer.stop()
