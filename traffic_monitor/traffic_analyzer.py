import sys
import os

# Add the root directory to the Python path
root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(root_dir)

from traffic_monitor.data_store import DataStore


class TrafficAnalyzer:
    def __init__(self, db_store):
        self.db_store = db_store
        self.unique_vehicles = set()


    def analyze_tpms_data(self, tpms_data):
        try:
            #print("Analyzing TPMS data:", tpms_data)
            print()
            # Your analysis logic here
        except Exception as e:
            print(f"Error during analysis: {e}")

        # Store data in the database
        try:
            self.db_store.insert_tpms_data(tpms_data)
        except Exception as e:
            print(f"Error storing TPMS data: {e}")
