import sqlite3

from hue.hue_connector import HueConnector
from hue.lights.hue_lights_handler import HueLightsHandler


class Migration:

    def __init__(self, lights_manager : HueLightsHandler):
        self.lights_manager = lights_manager

    def migrate(self):
        self.connection = sqlite3.connect('database/databases/smart_home.db')  # file path
        # create a cursor object from the cursor class
        cur = self.connection.cursor()
        self.create_tables_if_not_exist(cur)
        self.connection.commit()
        print("Database migrated")
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
                id INTEGER PRIMARY KEY,
                light_id INTEGER,
                state TEXT,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY(light_id) REFERENCES lights(id)
           )''')

        cur.execute('''
            CREATE TABLE IF NOT EXISTS switches(
                 id TEXT PRIMARY KEY,
                 name TEXT NOT NULL,
                 registration_date DATETIME DEFAULT CURRENT_TIMESTAMP
            )''')

        cur.execute('''
            CREATE TABLE IF NOT EXISTS switch_event_options(
                 id INTEGER PRIMARY KEY,
                 switch_id TEXT,
                 button_event TEXT,
                 event_type TEXT,
                 timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                 FOREIGN KEY(switch_id) REFERENCES switches(id)                 
            )''')

        cur.execute('''
            CREATE TABLE IF NOT EXISTS switch_event(
                 id integer,
                 event_timestamp TIMESTAMP,
                 switch_id TEXT,
                 switch_event_option_id INTEGER,
                 data_onboarded_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                 FOREIGN KEY(switch_id) REFERENCES switches(id)
                 FOREIGN KEY(switch_event_option_id) REFERENCES switch_event_options(id)
                 PRIMARY KEY(id,event_timestamp)
            )''')