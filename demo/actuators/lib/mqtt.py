from umqtt.simple import MQTTClient


class MQTT:
    def __init__(self, server, port, client_id, keepalive=30):
        self.server = server
        self.port = port
        self.client_id = client_id
        self.keepalive = keepalive

        self.client = MQTTClient(
            self.client_id,
            self.server,
            self.port,
            keepalive=self.keepalive
        )

        self.topics_sub = []

    def set_callback(self, callback):
        self.client.set_callback(callback)

    def subscribe(self, topic):
        print(f"Subscribing to '{topic}'")
        self.topics_sub.append(topic)
        self.client.subscribe(topic)

    def publish(self, topic, message):
        print(f"Publishing '{message}' to '{topic}'")
        self.client.publish(topic, str(message))

    def connect(self):
        print(f"Connecting to {self.server}:{self.port} as '{self.client_id}'")
        self.client.connect()
    
    def reconnect(self):
        print(f"Reconnecting to {self.server}:{self.port}")
        self.client.disconnect()
        self.client.connect()
        for topic in self.topics_sub:
            self.client.subscribe(topic)

    def receive_messages(self):
        while True:
            try:
                self.client.wait_msg()
            except Exception as e:
                print(f"Failed to receive message: {e}")
                self.reconnect()
