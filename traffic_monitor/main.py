import argparse
import sys
import os
import time
import schedule


# Add the root directory to the Python path
root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(root_dir)


from traffic_monitor.mqtt_client import MQTTClient
from traffic_monitor.traffic_analyzer import TrafficAnalyzer
from traffic_monitor.data_store import DataStore
from traffic_monitor.data_analysis import count_passing_cars, count_parked_cars


def parse_arguments():
    parser = argparse.ArgumentParser(description="Traffic Monitor using TPMS data.")
    parser.add_argument("--server", required=True, help="MQTT server address")
    parser.add_argument("--port", default=1883, type=int, help="MQTT server port")
    parser.add_argument("--username", help="MQTT username")
    parser.add_argument("--password", help="MQTT password")
    parser.add_argument("--topic", default="rtl_433/+/events", help="MQTT topic to subscribe to")
    return parser.parse_args()



def print_vehicle_counts(data_store, short_window, long_window):
    args = parse_arguments()
    mqtt_client = MQTTClient()
    mqtt_client.connect(args.server, args.port)

    if args.username and args.password:
        mqtt_client.authenticate(args.username, args.password)


    passing_car_count = count_passing_cars(data_store, short_window, long_window)
    parked_car_count = len(count_parked_cars(data_store, long_window))
    parked_vehicle_estimate = round(parked_car_count / 4)

    print(f"Passing cars in last {short_window} minutes: {passing_car_count}")
    print(f"Parked cars in last {long_window} minutes: {parked_vehicle_estimate}")
    # Publish the counts
    mqtt_client.publish("traffic/passingCars", passing_car_count)
    mqtt_client.publish("traffic/parkedCars", parked_vehicle_estimate)
    mqtt_client.disconnect()


def main():
    db_store = DataStore('/home/tom/database.db')

    args = parse_arguments()
    analyzer = TrafficAnalyzer(db_store)
    # Initialize and configure MQTT client
    schedule.every(0.1666).minutes.do(print_vehicle_counts, db_store, 5, 30)

    client = MQTTClient(on_tpms_message_callback=analyzer.analyze_tpms_data)


    client.connect(args.server, args.port)

    if args.username and args.password:
        client.authenticate(args.username, args.password)

    client.subscribe(args.topic)
    # Run indefinitely
    try:
        while True:
            schedule.run_pending()
            pass  # Or perform other tasks if needed
    except KeyboardInterrupt:
        print("Shutting down...")
        # Clean up operations if necessary

    # Here you can add logic to run your client indefinitely, handle interruptions, etc.

if __name__ == "__main__":
    main()

