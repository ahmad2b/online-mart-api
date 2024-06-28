import logging

from app.kafka.consumer.base import BaseConsumer

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class OrderItemConsumer(BaseConsumer):
    def __init__(self, bootstrap_servers, group_id):
        topics = ["order_item_created", "order_item_updated", "order_item_deleted"]
        super().__init__(topics, bootstrap_servers, group_id)

    def handle_message(self, message):
        event_type = message.get("type")
        if event_type == "order_item_created":
            self.handle_order_item_created(message["data"])
        elif event_type == "order_item_updated":
            self.handle_order_item_updated(message["data"])
        elif event_type == "order_item_deleted":
            self.handle_order_item_deleted(message["data"])

    def handle_order_item_created(self, data):
        logger.info(f"Order item created: {data}")

    def handle_order_item_updated(self, data):
        logger.info(f"Order item updated: {data}")

    def handle_order_item_deleted(self, data):
        logger.info(f"Order item deleted: {data}")
