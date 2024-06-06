import asyncio
from aiokafka import AIOKafkaConsumer

async def consume_messages(topics: list[str], bootstrap_servers: str, group_id: str):
    consumer = AIOKafkaConsumer( 
        *topics,
        bootstrap_servers=bootstrap_servers,
        group_id=group_id,
        auto_offset_reset='earliest'
    )

    await consumer.start()
    try:
        async for message in consumer:
            print(f"Received message: {message.value.decode()} on topic {message.topic}")
            # Process message
    finally:
        await consumer.stop()

from aiokafka import AIOKafkaConsumer
import json

class AuthEventConsumer:
    def __init__(self, kafka_servers):
        self.consumer = AIOKafkaConsumer(
            'auth_events',
            bootstrap_servers=kafka_servers,
            group_id="auth_event_group"
        )

    async def start(self):
        await self.consumer.start()

    async def stop(self):
        await self.consumer.stop()

    async def consume_events(self):
        async for msg in self.consumer:
            event = json.loads(msg.value)
            self.handle_event(event)

    def handle_event(self, event):
        if event["type"] == "user_registered":
            self.handle_user_registered(event["data"])
        elif event["type"] == "user_logged_in":
            self.handle_user_logged_in(event["data"])

    def handle_user_registered(self, data):
        # Handle user registered event
        pass

    def handle_user_logged_in(self, data):
        # Handle user logged in event
        pass
