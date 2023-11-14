import sqlite3
import os
from datetime import datetime, timedelta

class DataStore:
    def __init__(self, db_path):
        self.db_path = db_path
        self.initialize_database()

    def connect(self):
        return sqlite3.connect(self.db_path)


    def fetch_data(self, time_window_minutes):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        time_window = f"-{time_window_minutes} minutes"
        cursor.execute("SELECT id, timestamp FROM tpms_data WHERE timestamp >= datetime('now', ?) ORDER BY id, timestamp", (time_window,))
        data = cursor.fetchall()
        conn.close()
        return data

    def initialize_database(self):
        # Ensure the directory for the database file exists
        db_dir = os.path.dirname(self.db_path)
        if not os.path.exists(db_dir):
            os.makedirs(db_dir)

        try:
            self.create_tables()
        except sqlite3.Error as e:
            print(f"Error initializing database: {e}")
            raise


    def create_tables(self):
        with self.connect() as conn:
            conn.execute('''CREATE TABLE IF NOT EXISTS tpms_data (
                                entry_id INTEGER PRIMARY KEY AUTOINCREMENT,
                                id TEXT,
                                pressure REAL,
                                temperature REAL,
                                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
                            );''')
        print("Tables created or already exist.")

    def insert_tpms_data(self, tpms_data):
        with self.connect() as conn:
            #print("tpms data to insert:", tpms_data)
            conn.execute('''
                INSERT INTO tpms_data (id, pressure, temperature)
                VALUES (?, ?, ?);
                ''', (tpms_data['id'], tpms_data['pressure'], tpms_data['temperature']))

