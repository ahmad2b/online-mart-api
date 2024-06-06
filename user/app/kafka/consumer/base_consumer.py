from aiokafka import AIOKafkaConsumer
import json

class BaseConsumer:
    def __init__(self, topic, bootstrap_servers, group_id):
        self.consumer = AIOKafkaConsumer(
            topic,
            bootstrap_servers=bootstrap_servers,
            group_id=group_id,
            value_deserializer=lambda m: json.loads(m.decode('utf-8'))
        )

    async def start(self):
        await self.consumer.start()

    async def stop(self):
        await self.consumer.stop()

    async def consume(self):
        async for msg in self.consumer:
            self.handle_message(msg.value)

    def handle_message(self, message):
        raise NotImplementedError("handle_message() must be implemented by subclasses")
