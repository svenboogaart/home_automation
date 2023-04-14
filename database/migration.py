import sqlite3

from hue.hue_connector import HueConnector
from hue.lights.lights_manager import LightsManager


class Migration:

    def __init__(self, lights_manager : LightsManager):
        self.lights_manager = lights_manager

    def migrate(self):
        self.connection = sqlite3.connect('database/databases/smart_home.db')  # file path
        # create a cursor object from the cursor class
        cur = self.connection.cursor()
        self.create_tables_if_not_exist(cur)
        self.connection.commit()
        print("\nDatabase migrated successfully!!!")
        self.connection.close()
        # committing our connection

    def create_tables_if_not_exist(self, cur):
        cur.execute('''
           CREATE TABLE IF NOT EXISTS lights(
                id text PRIMARY KEY,
                name text NOT NULL,
                type text NOT NULL,
                registration_date DATETIME DEFAULT CURRENT_TIMESTAMP
           )''')

        cur.execute('''
           CREATE TABLE IF NOT EXISTS light_states(
                id integer PRIMARY KEY,
                light_id TEXT,
                state TEXT,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY(light_id) REFERENCES lights(id)
           )''')

