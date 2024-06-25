import logging

from app.kafka.consumer.base import BaseConsumer

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ProductConsumer(BaseConsumer):
    def __init__(self, bootstrap_servers, group_id):
        topics = ["product_created", "product_updated", "product_deleted"]
        super().__init__(topics, bootstrap_servers, group_id)

    def handle_message(self, message):
        event_type = message.get("type")
        if event_type == "product_created":
            self.handle_product_created(message["data"])
        elif event_type == "product_updated":
            self.handle_product_updated(message["data"])
        elif event_type == "product_deleted":
            self.handle_product_deleted(message["data"])

    def handle_product_created(self, data):
        logger.info(f"Product created: {data}")

    def handle_product_updated(self, data):
        logger.info(f"Product updated: {data}")

    def handle_product_deleted(self, data):
        logger.info(f"Product deleted: {data}")
