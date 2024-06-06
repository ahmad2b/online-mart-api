from app.kafka.consumer.base_consumer import BaseConsumer
from app.models import UserCreate
from sqlmodel import Session
from app.core.db import get_session
from app import crud

class UserConsumer(BaseConsumer):
    def __init__(self, bootstrap_servers, group_id):
        super().__init__("user_events", bootstrap_servers, group_id)

    async def handle_message(self, message):
        event_type = message.get("type")
        if event_type == "user_registered":
            await self.handle_user_registered(message["data"])
        elif event_type == "user_logged_in":
            await self.handle_user_logged_in(message["data"])

    async def handle_user_registered(self, data):
        async with get_session() as session:
            user_in = UserCreate(**data)
            crud.create_user(session=session, user_create=user_in)

    async def handle_user_logged_in(self, data):
        # Optionally handle login events, e.g., logging
        pass
