import json
from aiokafka import AIOKafkaProducer
from app.core.config import settings

class AdjustmentProducer:
    def __init__(self, bootstrap_servers=settings.BOOTSTRAP_SERVER):
        self.producer = AIOKafkaProducer(bootstrap_servers=bootstrap_servers)

    async def start(self):
        await self.producer.start()

    async def stop(self):
        await self.producer.stop()

    async def send(self, topic, message):
        await self.producer.send_and_wait(topic, json.dumps(message).encode('utf-8'))

    async def adjustment_made(self, adjustment_data):
        await self.send("adjustment_made", {"type": "adjustment_made", "data": adjustment_data})

# Dependency for FastAPI
async def get_adjustment_producer():
    producer = AdjustmentProducer()
    await producer.start()
    try:
        yield producer
    finally:
        await producer.stop()
