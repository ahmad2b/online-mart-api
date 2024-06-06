import json
from aiokafka import AIOKafkaProducer

class AuthProducer:
    def __init__(self, bootstrap_servers):
        self.producer = AIOKafkaProducer(bootstrap_servers=bootstrap_servers)

    async def start(self):
        await self.producer.start()

    async def stop(self):
        await self.producer.stop()

    async def send(self, topic, message):
        await self.producer.send_and_wait(topic, json.dumps(message).encode('utf-8'))

    async def register_user(self, user_data):
        await self.send("user_registered", user_data)

    async def login_user(self, login_data):

        data = {
            "user": login_data["email"],
            "token": login_data["token"]
        }
        await self.send("user_logged_in", data)
