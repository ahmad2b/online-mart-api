import logging

from app.kafka.consumer.base import BaseConsumer

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class CartItemConsumer(BaseConsumer):
    def __init__(self, bootstrap_servers, group_id):
        topics = ["cart_item_created", "cart_item_updated", "cart_item_deleted"]
        super().__init__(topics, bootstrap_servers, group_id)

    def handle_message(self, message):
        event_type = message.get("type")
        if event_type == "cart_item_created":
            self.handle_cart_item_created(message["data"])
        elif event_type == "cart_item_updated":
            self.handle_cart_item_updated(message["data"])
        elif event_type == "cart_item_deleted":
            self.handle_cart_item_deleted(message["data"])

    def handle_cart_item_created(self, data):
        logger.info(f"Cart Item created: {data}")

    def handle_cart_item_updated(self, data):
        logger.info(f"Cart Item updated: {data}")

    def handle_cart_item_deleted(self, data):
        logger.info(f"Cart Item deleted: {data}")
