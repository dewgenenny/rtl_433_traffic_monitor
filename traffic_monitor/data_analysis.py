import itertools
import sys
import os
from datetime import datetime, timedelta

# Add the root directory to the Python path
root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(root_dir)
from data_store import DataStore  # Import the DataStore class



def count_passing_cars(data_store, short_window_minutes, long_window_minutes):
    # Fetch data for the longer window to identify parked cars
    parked_cars = count_parked_cars(data_store, long_window_minutes)

    # Fetch data for the short window
    data = data_store.fetch_data(short_window_minutes)

    passing_cars = set()
    for id, group in itertools.groupby(data, lambda x: x[0]):
        if id not in parked_cars:
            timestamps = [datetime.strptime(ts, '%Y-%m-%d %H:%M:%S') for _, ts in group]
            if len(timestamps) == 1 or max(timestamps) - min(timestamps) <= timedelta(minutes=5):
                passing_cars.add(id)
    return len(passing_cars)

def count_parked_cars(data_store, time_window_minutes):
    data = data_store.fetch_data(time_window_minutes)
    parked_cars = set()
    for id, group in itertools.groupby(data, lambda x: x[0]):
        timestamps = [datetime.strptime(ts, '%Y-%m-%d %H:%M:%S') for _, ts in group]
        if len(timestamps) > 1 and max(timestamps) - min(timestamps) > timedelta(minutes=5):
            parked_cars.add(id)
    return parked_cars  # Return the set of parked car IDs

def estimate_vehicle_count(data_store, time_window_minutes, time_grouping_seconds=60):
    data = data_store.fetch_data(time_window_minutes)
    vehicles = set()

    for id, group in itertools.groupby(data, lambda x: x[0]):
        timestamps = [datetime.strptime(ts, '%Y-%m-%d %H:%M:%S') for _, ts in group]
        if len(timestamps) > 1:
            # Consider as a single vehicle if timestamps are close together
            if max(timestamps) - min(timestamps) <= timedelta(seconds=time_grouping_seconds):
                vehicles.add(id)

    # Assuming an average of 4 wheels per vehicle
    vehicle_count = round(len(vehicles) / 4)
    return vehicle_count
