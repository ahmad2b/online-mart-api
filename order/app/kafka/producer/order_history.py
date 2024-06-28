import json
from aiokafka import AIOKafkaProducer
from app.core.config import settings

class OrderHistoryProducer:
    def __init__(self, bootstrap_servers=settings.BOOTSTRAP_SERVER):
        self.producer = AIOKafkaProducer(bootstrap_servers=bootstrap_servers)

    async def start(self):
        await self.producer.start()

    async def stop(self):
        await self.producer.stop()

    async def send(self, topic, message):
        await self.producer.send_and_wait(topic, json.dumps(message).encode('utf-8'))

    async def order_history_created(self, order_history_data):
        await self.send("order_history_created", {"type": "order_history_created", "data": order_history_data})

    async def order_history_updated(self, order_history_data):
        await self.send("order_history_updated", {"type": "order_history_updated", "data": order_history_data})

    async def order_history_deleted(self, order_history_data):
        await self.send("order_history_deleted", {"type": "order_history_deleted", "data": order_history_data})

# Dependency for FastAPI
async def get_order_history_producer():
    producer = OrderHistoryProducer()
    await producer.start()
    try:
        yield producer
    finally:
        await producer.stop()
