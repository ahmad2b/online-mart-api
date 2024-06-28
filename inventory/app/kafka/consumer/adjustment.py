import logging

from app.kafka.consumer.base import BaseConsumer

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class AdjustmentConsumer(BaseConsumer):
    def __init__(self, bootstrap_servers, group_id):
        topics = ["adjustment_made"]
        super().__init__(topics, bootstrap_servers, group_id)

    def handle_message(self, message):
        event_type = message.get("type")
        if event_type == "adjustment_made":
            self.handle_adjustment_made(message["data"])

    def handle_adjustment_made(self, data):
        logger.info(f"Adjustment made: {data}")
