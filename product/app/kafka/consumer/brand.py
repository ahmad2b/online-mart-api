import logging

from app.kafka.consumer.base import BaseConsumer

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class BrandConsumer(BaseConsumer):
    def __init__(self, bootstrap_servers, group_id):
        topics = ["brand_created", "brand_updated", "brand_deleted"]
        super().__init__(topics, bootstrap_servers, group_id)

    def handle_message(self, message):
        event_type = message.get("type")
        if event_type == "brand_created":
            self.handle_brand_created(message["data"])
        elif event_type == "brand_updated":
            self.handle_brand_updated(message["data"])
        elif event_type == "brand_deleted":
            self.handle_brand_deleted(message["data"])

    def handle_brand_created(self, data):
        logger.info(f"Brand created: {data}")

    def handle_brand_updated(self, data):
        logger.info(f"Brand updated: {data}")

    def handle_brand_deleted(self, data):
        logger.info(f"Brand deleted: {data}")