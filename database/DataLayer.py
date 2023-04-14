import sqlite3
from typing import List

from sqlalchemy.orm import DeclarativeBase

from hue.lights.light import Light


class Base(DeclarativeBase):
    pass

class DataLayer:

    def __init__(self):
        self.connection = sqlite3.connect('/Users/Sven/Documents/programming/python/home_automation/database/databases/smart_home.db')  # file path

        # create a cursor object from the cursor class
        self.cur = self.connection.cursor()
        print("\nDatabase migrated successfully!!!")


    def store_lights(self, found_lights):
        insert_data = []
        try:
            for light in found_lights:
                print(light.unique_id)
                insert_data.append((light.unique_id, light.name, light.light_type))
            self.cur.executemany("INSERT INTO lights (id, name, type) VALUES(?, ?, ?)", insert_data)

            self.connection.commit()
        except Exception as e:
            # todo check which lights are new
            print("Already got the lights in the database")

    def get_light_states(self, light_id):
        light_states = []
        for row in self.cur.execute("SELECT state, timestamp FROM lights WHERE light_id = (?)", light_id).fetchall():
            light_states.append((row[0], row[1]))
        return light_states

    def log_light_states(self, lights: List[Light]):
        insert_data = []
        for light in lights:
            insert_data.append((light.unique_id, light.light_state.device_state.value))
        self.cur.executemany("INSERT INTO light_states (light_id, state) VALUES(?, ?)", insert_data)
        self.connection.commit()
