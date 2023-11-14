# traffic_monitor/mqtt_client.py
import paho.mqtt.client as mqtt
from .tpms_filter import TPMSFilter
import json

class MQTTClient:
    def __init__(self, on_tpms_message_callback=None):

        # Initialize the MQTT Client
        self.client = mqtt.Client()

        # Assign the on_message callback
        self.client.on_message = self._on_message

        # Initialize a list to store messages
        self._messages = []

        self.on_tpms_message_callback = on_tpms_message_callback


    def authenticate(self, username, password):
        self.client.username_pw_set(username, password)

    def connect(self, broker, port=1883):
        print(f"Connecting to MQTT Broker at {broker}:{port}")
        self.client.connect(broker, port)
        self.client.loop_start()

    def disconnect(self):
        self.client.disconnect()

    def subscribe(self, topic):
        # Subscribe to a topic
        print(f"Subscribing to topic: {topic}")
        self.client.subscribe(topic)

    def _on_message(self, client, userdata, message):
        # Decode the message payload
        message_payload = json.loads(message.payload.decode())


        # Use TPMSFilter to check if it's a TPMS message and process it
        if TPMSFilter.is_tpms_message(message_payload):
            tpms_data = TPMSFilter.extract_data(message_payload)
            if self.on_tpms_message_callback:
                #print("TPMS message detected, calling analyzer...")
                self.on_tpms_message_callback(tpms_data)

            #print(f"Received TPMS message: {tpms_data}")
        else:
            # Handle non-TPMS messages or simply ignore
            #print('.', end='', flush=True)
            pass

        self._messages.append(message.payload.decode())


    def publish(self, topic, value):
        # Convert the value to a JSON string if it's not a string already
        message = value if isinstance(value, str) else json.dumps(value)

        # Publish the message to the specified topic
        self.client.publish(topic, message)

    # Add any additional functionalities or utility methods as needed
