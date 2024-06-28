import logging

from app.kafka.consumer.base import BaseConsumer

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class InventoryConsumer(BaseConsumer):
    def __init__(self, bootstrap_servers, group_id):
        topics = ["inventory_created", "inventory_updated", "inventory_deleted"]
        super().__init__(topics, bootstrap_servers, group_id)

    def handle_message(self, message):
        event_type = message.get("type")
        if event_type == "inventory_created":
            self.handle_inventory_created(message["data"])
        elif event_type == "inventory_updated":
            self.handle_inventory_updated(message["data"])
        elif event_type == "inventory_deleted":
            self.handle_inventory_deleted(message["data"])

    def handle_inventory_created(self, data):
        logger.info(f"Inventory created: {data}")

    def handle_inventory_updated(self, data):
        logger.info(f"Inventory updated: {data}")

    def handle_inventory_deleted(self, data):
        logger.info(f"Inventory deleted: {data}")
