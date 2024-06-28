import logging

from app.kafka.consumer.base import BaseConsumer

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ReservationConsumer(BaseConsumer):
    def __init__(self, bootstrap_servers, group_id):
        topics = ["reservation_created", "reservation_updated", "reservation_deleted"]
        super().__init__(topics, bootstrap_servers, group_id)

    def handle_message(self, message):
        event_type = message.get("type")
        if event_type == "reservation_created":
            self.handle_reservation_created(message["data"])
        elif event_type == "reservation_updated":
            self.handle_reservation_updated(message["data"])
        elif event_type == "reservation_deleted":
            self.handle_reservation_deleted(message["data"])

    def handle_reservation_created(self, data):
        logger.info(f"Reservation created: {data}")

    def handle_reservation_updated(self, data):
        logger.info(f"Reservation updated: {data}")

    def handle_reservation_deleted(self, data):
        logger.info(f"Reservation deleted: {data}")
