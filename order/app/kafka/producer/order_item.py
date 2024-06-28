import json
from aiokafka import AIOKafkaProducer
from app.core.config import settings

class OrderItemProducer:
    def __init__(self, bootstrap_servers=settings.BOOTSTRAP_SERVER):
        self.producer = AIOKafkaProducer(bootstrap_servers=bootstrap_servers)

    async def start(self):
        await self.producer.start()

    async def stop(self):
        await self.producer.stop()

    async def send(self, topic, message):
        await self.producer.send_and_wait(topic, json.dumps(message).encode('utf-8'))

    async def order_item_created(self, order_item_data):
        await self.send("order_item_created", {"type": "order_item_created", "data": order_item_data})

    async def order_item_updated(self, order_item_data):
        await self.send("order_item_updated", {"type": "order_item_updated", "data": order_item_data})

    async def order_item_deleted(self, order_item_data):
        await self.send("order_item_deleted", {"type": "order_item_deleted", "data": order_item_data})

# Dependency for FastAPI
async def get_order_item_producer():
    producer = OrderItemProducer()
    await producer.start()
    try:
        yield producer
    finally:
        await producer.stop()
