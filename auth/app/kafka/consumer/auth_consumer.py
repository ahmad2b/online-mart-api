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

class AuthConsumer(BaseConsumer):
    def __init__(self, bootstrap_servers, group_id):
        super().__init__("auth_events", bootstrap_servers, group_id)

    def handle_message(self, message):
        event_type = message.get("type")
        if event_type == "user_deactivated":
            self.handle_user_deactivated(message["data"])
        elif event_type == "user_updated":
            self.handle_user_updated(message["data"])

    def handle_user_deactivated(self, data):
        # Handle user deactivated event
        print(f"User deactivated: {data}")

    def handle_user_updated(self, data):
        # Handle user updated event
        print(f"User updated: {data}")
