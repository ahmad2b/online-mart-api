import logging

from app.kafka.consumer.base import BaseConsumer

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ShippingDetailsConsumer(BaseConsumer):
    def __init__(self, bootstrap_servers, group_id):
        topics = ["shipping_details_created", "shipping_details_updated", "shipping_details_deleted"]
        super().__init__(topics, bootstrap_servers, group_id)

    def handle_message(self, message):
        event_type = message.get("type")
        if event_type == "shipping_details_created":
            self.handle_shipping_details_created(message["data"])
        elif event_type == "shipping_details_updated":
            self.handle_shipping_details_updated(message["data"])
        elif event_type == "shipping_details_deleted":
            self.handle_shipping_details_deleted(message["data"])

    def handle_shipping_details_created(self, data):
        logger.info(f"Shipping details created: {data}")

    def handle_shipping_details_updated(self, data):
        logger.info(f"Shipping details updated: {data}")

    def handle_shipping_details_deleted(self, data):
        logger.info(f"Shipping details deleted: {data}")
