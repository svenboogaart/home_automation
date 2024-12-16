import sqlite3
from typing import List

from sqlalchemy.orm import DeclarativeBase

from interfaces.lights.i_light import ILight
from interfaces.sensors.i_motion_sensor import IMotionSensor
from interfaces.sensors.i_switch import ISwitch


class Base(DeclarativeBase):
    pass


class DataLayer:

    def __init__(self):
        self.connection = sqlite3.connect(
            '/Users/Sven/Documents/programming/python/home_automation/database/databases/smart_home.db')  # file path

        # create a cursor object from the cursor class
        self.cur = self.connection.cursor()

    def store_lights(self, found_lights: List[ILight]):
        insert_data = []
        try:
            for light in found_lights:
                insert_data.append((light.get_unique_id(), light.get_name(), light.get_type()))
            self.cur.executemany("INSERT OR IGNORE  INTO lights (id, name, type) VALUES(?, ?, ?)", insert_data)

            self.connection.commit()
        except Exception as e:
            print("Already got the lights in the database")

    def log_light_state(self, light: ILight):
        insert_data = [(light.get_unique_id(), light.get_light_state().device_state.value,
                        light.get_light_state().brightness,
                        light.get_light_state().hue, light.get_light_state().saturation)]
        self.cur.executemany(
            "INSERT INTO light_states (light_id, state, brightness, hue, saturation) VALUES(?, ?, ?, ?, ?)",
            insert_data)
        self.connection.commit()

    def store_switches(self, switches: List[ISwitch]):
        insert_data = []
        try:
            for switch in switches:
                insert_data.append((switch.get_unique_id(), switch.get_name()))
            self.cur.executemany("INSERT OR IGNORE INTO switches (id, name) VALUES(?, ?)", insert_data)

            self.connection.commit()
        except Exception as e:
            print("Already got the switches in the database. ", e)

    def log_switch_event(self, switch: ISwitch):
        insert_data = [
            (switch.get_unique_id(),
             switch.get_last_update_date(),
             int(switch.is_pressed_event()),
             int(switch.is_hold_event()),
             int(switch.is_released_event()),
             int(switch.is_release_long_click()),
             123
             )]
        self.cur.executemany(
            "INSERT INTO switch_event (switch_id, last_updated, button_pressed, hold, release, release_hold, "
            "button_event) VALUES(?, ?, ?, ?, ? ,?, ?)",
            insert_data)
        self.connection.commit()

    def log_motion_sensors(self, motion_sensors: List[IMotionSensor]):
        insert_data = []
        try:
            for sensor in motion_sensors:
                insert_data.append((sensor.get_unique_id(), sensor.get_name()))
            self.cur.executemany("INSERT OR IGNORE INTO motion_sensors (id, name) VALUES(?, ?)", insert_data)

            self.connection.commit()
        except Exception as e:
            print("Failed to insert switch. ", e)

    def log_motion_sensor_event(self, motion_sensor: IMotionSensor):
        insert_data = [
            (motion_sensor.get_unique_id(), int(motion_sensor.motion_detected()), motion_sensor.get_last_update_date())]
        self.cur.executemany(
            "INSERT INTO motion_sensor_events (motion_sensor_id, presence_detected, last_updated) VALUES(?, ?, ?)",
            insert_data)
        self.connection.commit()
