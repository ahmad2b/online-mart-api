from app.core.config import settings
from app.kafka.producer.auth_producer import AuthProducer

from app.kafka.consumer.user_consumer import UserConsumer
from app.kafka.consumer.auth_consumer import AuthConsumer

async def get_auth_producer():
    producer = AuthProducer(settings.BOOTSTRAP_SERVER)
    await producer.start()
    try:
        yield producer
    finally:
        await producer.stop()


async def get_user_consumer():
    consumer = UserConsumer(settings.BOOTSTRAP_SERVER, "user_service_group")
    await consumer.start()
    try:
        yield consumer
    finally:
        await consumer.stop()

async def get_auth_consumer():
    consumer = AuthConsumer(settings.BOOTSTRAP_SERVER, "auth_service_group")
    await consumer.start()
    try:
        yield consumer
    finally:
        await consumer.stop()