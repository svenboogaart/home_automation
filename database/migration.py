import os
import sqlite3


class Migration:

    def __init__(self):
        self.connection = None

    def migrate(self):
        path = 'databases/smart_home.db'
        scriptdir = os.path.dirname(__file__)
        # add the relative path to the database file from there
        db_path = os.path.join(scriptdir, path)
        self.connection = sqlite3.connect(db_path)  # file path
        # create a cursor object from the cursor class
        cur = self.connection.cursor()
        self.create_tables_if_not_exist(cur)
        self.connection.commit()
        print("Database migrated")
        self.connection.close()
        # committing our connection

    @staticmethod
    def create_tables_if_not_exist(cur):
        cur.execute('''
           CREATE TABLE IF NOT EXISTS lights(
                id text PRIMARY KEY,
                name text NOT NULL,
                type text NOT NULL,
                registration_date DATETIME DEFAULT CURRENT_TIMESTAMP
           )''')

        cur.execute('''
           CREATE TABLE IF NOT EXISTS light_states(
                light_id INTEGER,
                brightness INTEGER,
                hue INTEGER,
                saturation INTEGER,
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
            CREATE TABLE IF NOT EXISTS switch_event(    
                 id INTEGER PRIMARY KEY  AUTOINCREMENT,
                 switch_id TEXT,
                 last_updated TIMESTAMP,
                 button_pressed INTEGER,
                 hold INTEGER,
                 release INTEGER,
                 release_hold INTEGER,
                 button_event INTEGER,
                 data_onboarded_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                 FOREIGN KEY(switch_id) REFERENCES switches(id)
            )''')

        cur.execute('''
            CREATE TABLE IF NOT EXISTS motion_sensors(
                 id TEXT PRIMARY KEY,
                 name TEXT NOT NULL,
                 registration_date DATETIME DEFAULT CURRENT_TIMESTAMP
            )''')

        cur.execute('''
            CREATE TABLE IF NOT EXISTS motion_sensor_events(  
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                motion_sensor_id TEXT,
                presence_detected integer,
                last_updated TIMESTAMP, 
                data_onboarded_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY(motion_sensor_id) REFERENCES motion_sensors(id)
            )''')

        cur.execute('''
                    CREATE TABLE IF NOT EXISTS daylight_sensors(
                         id TEXT PRIMARY KEY,
                         name TEXT NOT NULL,
                         registration_date DATETIME DEFAULT CURRENT_TIMESTAMP
                    )''')

        cur.execute('''
                    CREATE TABLE IF NOT EXISTS daylight_sensor_events(  
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        daylight_sensor_id TEXT,
                        daylight_detected integer,
                        last_updated TIMESTAMP, 
                        data_onboarded_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        FOREIGN KEY(daylight_sensor_id) REFERENCES daylight_sensors(id)
                    )''')

        cur.execute('''
                    CREATE TABLE IF NOT EXISTS temperature_sensors(
                         id TEXT PRIMARY KEY,
                         name TEXT NOT NULL,
                         registration_date DATETIME DEFAULT CURRENT_TIMESTAMP
                    )''')

        cur.execute('''
                    CREATE TABLE IF NOT EXISTS temperature_sensor_events(  
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        temperature_sensor_id TEXT,
                        temperature REAL,
                        last_updated TIMESTAMP, 
                        data_onboarded_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        FOREIGN KEY(temperature_sensor_id) REFERENCES temperature_sensors(id)
                    )''')

        cur.execute('''
                    CREATE TABLE IF NOT EXISTS contact_sensors(
                         id TEXT PRIMARY KEY,
                         name TEXT NOT NULL,
                         registration_date DATETIME DEFAULT CURRENT_TIMESTAMP
                    )''')

        cur.execute('''
                    CREATE TABLE IF NOT EXISTS contact_sensor_events(  
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        contact_sensor_id TEXT,
                        has_contact int,
                        last_updated TIMESTAMP, 
                        data_onboarded_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        FOREIGN KEY(contact_sensor_id) REFERENCES contact_sensors(id)
                    )''')
