from aiokafka import AIOKafkaConsumer
import json

import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class BaseConsumer:
    def __init__(self, topics, bootstrap_servers, group_id):
        self.consumer = AIOKafkaConsumer(
            *topics,  # Unpack the list of topics
            bootstrap_servers=bootstrap_servers,
            group_id=group_id,
            value_deserializer=lambda m: json.loads(m.decode('utf-8'))
        )

    async def start(self):
        await self.consumer.start()
        logger.info("Consumer started")


    async def stop(self):
        await self.consumer.stop()
        logger.info("Consumer stopped")

    async def consume(self):
        try:
            async for msg in self.consumer:
                logger.info(f"Consumed message: {msg.value}")
                self.handle_message(msg.value)
        except Exception as e:
            logger.error(f"Error consuming messages: {e}")

    def handle_message(self, message):
        raise NotImplementedError("handle_message() must be implemented by subclasses")

class UserConsumer(BaseConsumer):
    def __init__(self, bootstrap_servers, group_id):
        topics = ["user_registered", "user_logged_in"]
        super().__init__(topics, bootstrap_servers, group_id)

    def handle_message(self, message):
        event_type = message.get("type")
        if event_type == "user_registered":
            self.handle_user_registered(message["data"])
        elif event_type == "user_logged_in":
            self.handle_user_logged_in(message["data"])

    def handle_user_registered(self, data):
        # Handle user registered event
        print(f"User registered: {data}")
        logger.info(f"User registered: {data}")


    def handle_user_logged_in(self, data):
        # Handle user logged in event
        print(f"User logged in: {data}")
        logger.info(f"User logged in: {data}")

