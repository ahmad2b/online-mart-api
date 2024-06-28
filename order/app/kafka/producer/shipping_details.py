import json
from aiokafka import AIOKafkaProducer
from app.core.config import settings

class ShippingDetailsProducer:
    def __init__(self, bootstrap_servers=settings.BOOTSTRAP_SERVER):
        self.producer = AIOKafkaProducer(bootstrap_servers=bootstrap_servers)

    async def start(self):
        await self.producer.start()

    async def stop(self):
        await self.producer.stop()

    async def send(self, topic, message):
        await self.producer.send_and_wait(topic, json.dumps(message).encode('utf-8'))

    async def shipping_details_created(self, shipping_details_data):
        await self.send("shipping_details_created", {"type": "shipping_details_created", "data": shipping_details_data})

    async def shipping_details_updated(self, shipping_details_data):
        await self.send("shipping_details_updated", {"type": "shipping_details_updated", "data": shipping_details_data})

    async def shipping_details_deleted(self, shipping_details_data):
        await self.send("shipping_details_deleted", {"type": "shipping_details_deleted", "data": shipping_details_data})

# Dependency for FastAPI
async def get_shipping_details_producer():
    producer = ShippingDetailsProducer()
    await producer.start()
    try:
        yield producer
    finally:
        await producer.stop()
