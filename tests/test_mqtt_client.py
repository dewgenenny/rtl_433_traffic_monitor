# tests/test_mqtt_client.py
import pytest
from unittest.mock import patch, MagicMock
from traffic_monitor.mqtt_client import MQTTClient
from traffic_monitor.tpms_filter import TPMSFilter

# Mocking the paho MQTT Client
@patch("traffic_monitor.mqtt_client.mqtt.Client")
def test_connect_to_broker(mock_mqtt_client):
    # Mock the connect method
    mock_instance = mock_mqtt_client.return_value
    mock_instance.connect.return_value = None

    # Instantiate your MQTTClient and call the connect method
    client = MQTTClient()
    client.connect("broker.hivemq.com", 1883)  # Example broker address and port

    # Ensure connect method was called with correct parameters
    mock_instance.connect.assert_called_with("broker.hivemq.com", 1883)

@patch("traffic_monitor.mqtt_client.mqtt.Client")
def test_subscribe_to_topic(mock_mqtt_client):
    # Mock the subscribe method
    mock_instance = mock_mqtt_client.return_value
    mock_instance.subscribe.return_value = None

    # Instantiate your MQTTClient and call the subscribe method
    client = MQTTClient()
    client.subscribe("rtl_433/+/events")  # Example topic

    # Ensure subscribe method was called with correct parameters
    mock_instance.subscribe.assert_called_with("rtl_433/+/events")

@patch("traffic_monitor.mqtt_client.mqtt.Client")
def test_receive_message(mock_mqtt_client):
    # Create a mock message with example payload
    example_payload = '{"time":"2023-11-11 09:34:50","model":"Toyota","type":"TPMS","id":"f15e3929"}'
    mock_message = MagicMock()
    mock_message.payload.decode.return_value = example_payload

    # Instantiate your MQTTClient
    client = MQTTClient()

    # Simulate receiving a message
    client._on_message(None, None, mock_message)

    # Check if the message was added to the list
    assert client._messages[-1] == example_payload

# Mock TPMSFilter to control its behavior in the tests
@patch('traffic_monitor.mqtt_client.TPMSFilter')
def test_process_tpms_message(mock_tpms_filter):
    # Setup mock for TPMSFilter
    mock_tpms_filter.is_tpms_message.return_value = True
    mock_tpms_filter.extract_data.return_value = {'id': 'f15e3929', 'pressure': '32.25 PSI'}

    # Create a mock MQTT message
    example_payload = '{"type":"TPMS","id":"f15e3929","pressure_PSI":32.25}'
    mock_message = MagicMock()
    mock_message.payload.decode.return_value = example_payload

    # Initialize MQTTClient and simulate message reception
    client = MQTTClient()
    client._on_message(None, None, mock_message)

    # Assert TPMSFilter methods were called correctly
    mock_tpms_filter.is_tpms_message.assert_called_once()
    mock_tpms_filter.extract_data.assert_called_once_with({'type': 'TPMS', 'id': 'f15e3929', 'pressure_PSI': 32.25})

    # You can also test if the client processes the extracted data correctly, depending on your implementation

@patch('traffic_monitor.mqtt_client.TPMSFilter')
def test_process_non_tpms_message(mock_tpms_filter):
    # Make sure the mock is set up correctly
    mock_tpms_filter.is_tpms_message.return_value = False

    # Create a mock MQTT message that is not a TPMS message
    example_payload = '{"type":"Other","id":"12345678"}'
    mock_message = MagicMock()
    mock_message.payload.decode.return_value = example_payload

    # Initialize MQTTClient and simulate message reception
    client = MQTTClient()
    client._on_message(None, None, mock_message)

    # Assert TPMSFilter.is_tpms_message was called, but extract_data was not
    mock_tpms_filter.is_tpms_message.assert_called_once()
    mock_tpms_filter.extract_data.assert_not_called()
