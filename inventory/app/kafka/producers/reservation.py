import json
from aiokafka import AIOKafkaProducer
from app.core.config import settings

class ReservationProducer:
    def __init__(self, bootstrap_servers=settings.BOOTSTRAP_SERVER):
        self.producer = AIOKafkaProducer(bootstrap_servers=bootstrap_servers)

    async def start(self):
        await self.producer.start()

    async def stop(self):
        await self.producer.stop()

    async def send(self, topic, message):
        await self.producer.send_and_wait(topic, json.dumps(message).encode('utf-8'))

    async def reservation_created(self, reservation_data):
        await self.send("reservation_created", {"type": "reservation_created", "data": reservation_data})

    async def reservation_updated(self, reservation_data):
        await self.send("reservation_updated", {"type": "reservation_updated", "data": reservation_data})

    async def reservation_deleted(self, reservation_data):
        await self.send("reservation_deleted", {"type": "reservation_deleted", "data": reservation_data})

# Dependency for FastAPI
async def get_reservation_producer():
    producer = ReservationProducer()
    await producer.start()
    try:
        yield producer
    finally:
        await producer.stop()
