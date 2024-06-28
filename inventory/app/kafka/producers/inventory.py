import json
from aiokafka import AIOKafkaProducer
from app.core.config import settings

class InventoryProducer:
    def __init__(self, bootstrap_servers=settings.BOOTSTRAP_SERVER):
        self.producer = AIOKafkaProducer(bootstrap_servers=bootstrap_servers)

    async def start(self):
        await self.producer.start()

    async def stop(self):
        await self.producer.stop()

    async def send(self, topic, message):
        await self.producer.send_and_wait(topic, json.dumps(message).encode('utf-8'))
        
    async def inventory_created(self, inventory_data):
        await self.send("inventory_created", {"type": "inventory_created", "data": inventory_data})


    async def inventory_updated(self, inventory_data):
        await self.send("inventory_updated", {"type": "inventory_updated", "data": inventory_data})
        
    async def inventory_deleted(self, inventory_data):
        await self.send("inventory_deleted", {"type": "inventory_deleted", "data": inventory_data})


# Dependency for FastAPI
async def get_inventory_producer():
    producer = InventoryProducer()
    await producer.start()
    try:
        yield producer
    finally:
        await producer.stop()
