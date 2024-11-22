import sqlite3
from typing import List

from sqlalchemy.orm import DeclarativeBase

from models.lights.light import Light
from models.sensors.motion_sensor import MotionSensor
from models.sensors.switch import Switch


class Base(DeclarativeBase):
    pass


class DataLayer:

    def __init__(self):
        self.connection = sqlite3.connect(
            '/Users/Sven/Documents/programming/python/home_automation/database/databases/smart_home.db')  # file path

        # create a cursor object from the cursor class
        self.cur = self.connection.cursor()

    def store_lights(self, found_lights):
        insert_data = []
        try:
            for light in found_lights:
                insert_data.append((light.unique_id, light.name, light.light_type))
            self.cur.executemany("INSERT OR IGNORE  INTO lights (id, name, type) VALUES(?, ?, ?)", insert_data)

            self.connection.commit()
        except Exception as e:
            # todo check which lights are new
            print("Already got the lights in the database")

    def store_switches(self, switches: List[Switch]):
        insert_data = []
        try:
            for switch in switches:
                insert_data.append((switch.unique_id, switch.name))
            self.cur.executemany("INSERT OR IGNORE INTO switches (id, name) VALUES(?, ?)", insert_data)

            self.connection.commit()
        except Exception as e:
            # todo check which switches are new
            print("Already got the switches in the database. ", e)

    def log_switch_event(self, switch: Switch):
        insert_data = [
            (switch.unique_id,
             switch.state.last_updated,
             int(switch.state.button_pressed),
             int(switch.state.hold),
             int(switch.state.release),
             int(switch.state.release_hold),
             switch.state.button_event
             )]
        self.cur.executemany(
            "INSERT INTO switch_event (switch_id, last_updated, button_pressed, hold, release, release_hold, button_event) VALUES(?, ?, ?, ?, ? ,?, ?)",
            insert_data)
        self.connection.commit()

    def store_motion_sensors(self, switches: List[Switch]):
        insert_data = []
        try:
            for switch in switches:
                insert_data.append((switch.unique_id, switch.name))
            self.cur.executemany("INSERT OR IGNORE INTO switches (id, name) VALUES(?, ?)", insert_data)

            self.connection.commit()
        except Exception as e:
            # todo check which switches are new
            print("Already got the switches in the database. ", e)

    #
    # def get_light_states(self, light_id):
    #     light_states = []
    #     for row in self.cur.execute("SELECT state, timestamp FROM lights WHERE light_id = (?)", light_id).fetchall():
    #         light_states.append((row[0], row[1]))
    #     return light_states

    def log_light_state(self, light: Light):
        insert_data = [(light.unique_id, light.light_state.device_state.value, light.light_state.brightness,
                        light.light_state.hue, light.light_state.saturation)]
        self.cur.executemany(
            "INSERT INTO light_states (light_id, state, brightness, hue, saturation) VALUES(?, ?, ?, ?, ?)",
            insert_data)
        self.connection.commit()

    def log_motion_sensors(self, motion_sensors: List[MotionSensor]):
        insert_data = []
        try:
            for sensor in motion_sensors:
                insert_data.append((sensor.unique_id, sensor.name))
            self.cur.executemany("INSERT OR IGNORE INTO motion_sensors (id, name) VALUES(?, ?)", insert_data)

            self.connection.commit()
        except Exception as e:
            print("Failed to insert switch. ", e)

    def log_motion_sensor_event(self, motion_sensor: MotionSensor):
        insert_data = [(motion_sensor.unique_id, int(motion_sensor.state.presence), motion_sensor.state.last_updated)]
        self.cur.executemany(
            "INSERT INTO motion_sensor_events (motion_sensor_id, presence_detected, last_updated) VALUES(?, ?, ?)",
            insert_data)
        self.connection.commit()
