import logging

from app.kafka.consumer.base import BaseConsumer

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class CategoryConsumer(BaseConsumer):
    def __init__(self, bootstrap_servers, group_id):
        topics = ["category_created", "category_updated", "category_deleted"]
        super().__init__(topics, bootstrap_servers, group_id)

    def handle_message(self, message):
        event_type = message.get("type")
        if event_type == "category_created":
            self.handle_category_created(message["data"])
        elif event_type == "category_updated":
            self.handle_category_updated(message["data"])
        elif event_type == "category_deleted":
            self.handle_category_deleted(message["data"])

    def handle_category_created(self, data):
        logger.info(f"Category created: {data}")

    def handle_category_updated(self, data):
        logger.info(f"Category updated: {data}")

    def handle_category_deleted(self, data):
        logger.info(f"Category deleted: {data}")
