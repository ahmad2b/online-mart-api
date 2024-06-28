import logging
from app.kafka.consumer.base import BaseConsumer

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class OrderConsumer(BaseConsumer):
    def __init__(self, bootstrap_servers, group_id):
        topics = ["order_created", "order_updated", "order_deleted"]
        super().__init__(topics, bootstrap_servers, group_id)

    def handle_message(self, message):
        event_type = message.get("type")
        if event_type == "order_created":
            self.handle_order_created(message["data"])
        elif event_type == "order_updated":
            self.handle_order_updated(message["data"])
        elif event_type == "order_deleted":
            self.handle_order_deleted(message["data"])

    def handle_order_created(self, data):
        logger.info(f"Order created: {data}")

    def handle_order_updated(self, data):
        logger.info(f"Order updated: {data}")

    def handle_order_deleted(self, data):
        logger.info(f"Order deleted: {data}")
