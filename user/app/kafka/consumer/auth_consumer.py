from app.kafka.consumer.base_consumer import BaseConsumer

class AuthConsumer(BaseConsumer):
    def __init__(self, bootstrap_servers, group_id):
        super().__init__("auth_events", bootstrap_servers, group_id)

    def handle_message(self, message):
        event_type = message.get("type")
        if event_type == "user_registered":
            self.handle_user_registered(message["data"])
        elif event_type == "user_logged_in":
            self.handle_user_logged_in(message["data"])

    def handle_user_registered(self, data):
        # Handle user registered event
        print(f"User registered: {data}")

    def handle_user_logged_in(self, data):
        # Handle user logged in event
        print(f"User logged in: {data}")
