import logging

from app.kafka.consumer.base import BaseConsumer

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class OrderHistoryConsumer(BaseConsumer):
    def __init__(self, bootstrap_servers, group_id):
        topics = ["order_history_created", "order_history_updated", "order_history_deleted"]
        super().__init__(topics, bootstrap_servers, group_id)

    def handle_message(self, message):
        event_type = message.get("type")
        if event_type == "order_history_created":
            self.handle_order_history_created(message["data"])
        elif event_type == "order_history_updated":
            self.handle_order_history_updated(message["data"])
        elif event_type == "order_history_deleted":
            self.handle_order_history_deleted(message["data"])

    def handle_order_history_created(self, data):
        logger.info(f"Order history created: {data}")

    def handle_order_history_updated(self, data):
        logger.info(f"Order history updated: {data}")

    def handle_order_history_deleted(self, data):
        logger.info(f"Order history deleted: {data}")
