import json
from aiokafka import AIOKafkaConsumer
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class BaseConsumer:
    def __init__(self, topics, bootstrap_servers, group_id):
        self.consumer = AIOKafkaConsumer(
            *topics,
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
