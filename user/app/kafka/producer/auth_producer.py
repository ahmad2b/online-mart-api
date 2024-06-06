from app.core import security
from app.kafka.producer.base_producer import BaseProducer

class AuthProducer(BaseProducer):
    def __init__(self, bootstrap_servers):
        super().__init__(bootstrap_servers)

    async def register_user(self, user_data):
        await self.send("user_registered", user_data)

    async def login_user(self, login_data):
        token = security.create_access_token(login_data)
        data = {
            "user": login_data,
            "token": token
        }
        await self.send("user_logged_in", data)
        return token
