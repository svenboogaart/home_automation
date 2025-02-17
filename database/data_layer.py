import os
import sqlite3
from typing import List, Tuple

from interfaces.lights.i_light import ILight
from interfaces.sensors.i_contact_sensor import IContactSensor
from interfaces.sensors.i_daylight_sensor import IDaylightSensor
from interfaces.sensors.i_motion_sensor import IMotionSensor
from interfaces.sensors.i_switch import ISwitch
from interfaces.sensors.i_temperature_sensor import ITemperatureSensor


class DataLayer:
    def __init__(self):
        path = 'databases/smart_home.db'
        script_dir = os.path.dirname(__file__)
        # add the relative path to the database file from there
        db_path = os.path.join(script_dir, path)
        self.connection = sqlite3.connect(db_path)  # file path

        # create a cursor object from the cursor class
        self.cur = self.connection.cursor()

    def store_lights(self, found_lights: List[ILight]):
        insert_data = []
        for light in found_lights:
            insert_data.append((light.get_unique_id(), light.get_name(), light.get_type()))

        query = "INSERT OR IGNORE  INTO lights (id, name, type) VALUES(?, ?, ?)"
        self._execute_insert(query, insert_data)

    def log_light_state(self, light: ILight):
        insert_data = [(light.get_unique_id(), light.get_light_state().device_state.value,
                        light.get_light_state().brightness,
                        light.get_light_state().hue, light.get_light_state().saturation)]
        self._execute_insert(
            "INSERT INTO light_states (light_id, state, brightness, hue, saturation) VALUES(?, ?, ?, ?, ?)",
            insert_data)

    def store_switches(self, switches: List[ISwitch]):
        insert_data = []
        for switch in switches:
            insert_data.append((switch.get_unique_id(), switch.get_name()))
        self.cur.executemany("INSERT OR IGNORE INTO switches (id, name) VALUES(?, ?)", insert_data)

        query = "INSERT OR IGNORE INTO switches (id, name) VALUES(?, ?)"
        self._execute_insert(query, insert_data)

    def log_switch_event(self, switch: ISwitch):
        insert_data = [
            (switch.get_unique_id(),
             switch.get_last_update_date(),
             int(switch.is_pressed_event()),
             int(switch.is_hold_event()),
             int(switch.is_released_event()),
             int(switch.is_release_long_click()),
             switch.get_last_event_code()
             )]

        query = ("INSERT INTO switch_event (switch_id, last_updated, button_pressed, hold, release, release_hold, "
                 "button_event) VALUES(?, ?, ?, ?, ? ,?, ?)")
        self._execute_insert(query, insert_data)

    def log_motion_sensors(self, motion_sensors: List[IMotionSensor]):
        insert_data = []
        for sensor in motion_sensors:
            insert_data.append((sensor.get_unique_id(), sensor.get_name()))

        query = "INSERT OR IGNORE INTO motion_sensors (id, name) VALUES(?, ?)"
        self._execute_insert(query, insert_data)

    def log_daylight_sensors(self, sensors: List[IDaylightSensor]):
        insert_data = []
        for sensor in sensors:
            insert_data.append((sensor.get_unique_id(), sensor.get_name()))

        query = "INSERT OR IGNORE INTO daylight_sensors (id, name) VALUES(?, ?)"
        self._execute_insert(query, insert_data)

    def log_temperature_sensors(self, sensors: List[ITemperatureSensor]):
        insert_data = []
        for sensor in sensors:
            insert_data.append((sensor.get_unique_id(), sensor.get_name()))

        query = "INSERT OR IGNORE INTO temperature_sensors (id, name) VALUES(?, ?)"
        self._execute_insert(query, insert_data)

    def log_contact_sensors(self, sensors: List[IContactSensor]):
        insert_data = []
        for sensor in sensors:
            insert_data.append((sensor.get_unique_id(), sensor.get_name()))

        query = "INSERT OR IGNORE INTO contact_sensors (id, name) VALUES(?, ?)"
        self._execute_insert(query, insert_data)

    def log_motion_sensor_event(self, motion_sensor: IMotionSensor):
        insert_data = [
            (motion_sensor.get_unique_id(), int(motion_sensor.motion_detected()), motion_sensor.get_last_update_date())]
        query = "INSERT INTO motion_sensor_events (motion_sensor_id, presence_detected, last_updated) VALUES(?, ?, ?)"
        self._execute_insert(query, insert_data)

    def log_daylight_sensor_event(self, sensor: IDaylightSensor):
        insert_data = [
            (sensor.get_unique_id(), int(sensor.daylight_detected()), sensor.get_last_update_date())]
        query = "INSERT INTO daylight_sensor_events (daylight_sensor_id, daylight_detected, last_updated) VALUES(?, ?, ?)"
        self._execute_insert(query, insert_data)

    def log_temperature_sensor_event(self, sensor: ITemperatureSensor):
        insert_data = [
            (sensor.get_unique_id(), round(sensor.get_temperature(), 2), sensor.get_last_update_date())]
        query = "INSERT INTO temperature_sensor_events (temperature_sensor_id, temperature, last_updated) VALUES(?, ?, ?)"
        self._execute_insert(query, insert_data)

    def log_contact_sensor_event(self, sensor: IContactSensor):
        insert_data = [
            (sensor.get_unique_id(), int(sensor.has_contact()), sensor.get_last_update_date())]
        query = "INSERT INTO contact_sensor_events (contact_sensor_id, has_contact, last_updated) VALUES(?, ?, ?)"
        self._execute_insert(query, insert_data)

    def _execute_insert(self, query: str, data: List[Tuple]):
        try:
            self.cur.executemany(query, data)
            self.connection.commit()
        except sqlite3.IntegrityError as e:
            # Handle specific integrity errors (e.g., constraint violations)
            print(f"Integrity error: {e}")
        except sqlite3.DatabaseError as e:
            # Simple error handling with a basic print statement
            print(f"Database error: {e}")
        except Exception as e:
            # Catch all other unexpected exceptions
            print(f"Unexpected error: {e}")
