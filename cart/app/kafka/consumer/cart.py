import logging

from app.kafka.consumer.base import BaseConsumer

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class CartConsumer(BaseConsumer):
    def __init__(self, bootstrap_servers, group_id):
        topics = ["cart_created", "cart_updated", "cart_deleted"]
        super().__init__(topics, bootstrap_servers, group_id)

    def handle_message(self, message):
        event_type = message.get("type")
        if event_type == "cart_created":
            self.handle_cart_created(message["data"])
        elif event_type == "cart_updated":
            self.handle_cart_updated(message["data"])
        elif event_type == "cart_deleted":
            self.handle_cart_deleted(message["data"])

    def handle_cart_created(self, data):
        logger.info(f"Cart created: {data}")

    def handle_cart_updated(self, data):
        logger.info(f"Cart updated: {data}")

    def handle_cart_deleted(self, data):
        logger.info(f"Cart deleted: {data}")
