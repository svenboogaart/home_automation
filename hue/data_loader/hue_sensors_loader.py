import json
import time
from typing import List

from helpers.enums.sensor_types import SensorType
from helpers.hue_event_helper import HueEventHelper
from hue.hue_connector import HueConnector
from hue.hue_data_loader_abc import HueDataLoaderAbc
from hue.sensors.hue_daylight_sensor import HueDayLightSensor
from hue.sensors.hue_motion_sensor import HueMotionSensor
from hue.sensors.hue_switch import HueSwitch, SwitchState
from hue.sensors.hue_temperature_sensor import HueTemperatureSensor
from interfaces.sensors.i_daylight_sensor import DayLightSensorState
from interfaces.sensors.i_temperature_sensor import TemperatureSensorState


# pylint: disable=W0246
class HueSensorsLoader(HueDataLoaderAbc):

    def __init__(self, hue_connector: HueConnector):
        super().__init__(hue_connector)

    def get_switches(self) -> List[HueSwitch]:
        switches = []
        for index, switch_data in self.get_sensor_json(SensorType.SWITCH).items():
            switches.append(self.__create_switch_sensor_from_json(index, switch_data))
        return switches

    def get_motion_sensors(self) -> List[HueMotionSensor]:
        motion_sensors = []
        for index, switch_data in self.get_sensor_json(SensorType.MOTION).items():
            motion_sensors.append(self.__create_motion_sensor_from_json(index, switch_data))
        return motion_sensors

    def get_daylight_sensors(self) -> List[HueDayLightSensor]:
        sensors = []
        for index, sensor_data in self.get_sensor_json(SensorType.DAYLIGHT).items():
            sensors.append(self.__create_daylight_sensor_from_json(index, sensor_data))
        return sensors

    def get_temperature_sensors(self) -> List[HueTemperatureSensor]:
        sensors = []
        for index, sensor_data in self.get_sensor_json(SensorType.TEMPERATURE).items():
            sensors.append(self.__create_temperature_sensor_from_json(index, sensor_data))
        return sensors

    def get_sensor_json(self, sensor_type: SensorType = None):
        sensors_json = {}
        try:
            sensor_data = self.hue_connector.run_get_request("sensors")
            if sensor_data:
                sensors_from_json = json.loads(sensor_data)
                for key, json_sensor in sensors_from_json.items():
                    if sensor_type:
                        json_sensor_type = json_sensor["type"]
                        sensor_type_enum_from_json = HueEventHelper.get_sensor_enum_from_string(json_sensor_type)
                        if sensor_type == sensor_type_enum_from_json:
                            sensors_json[key] = json_sensor
                    else:
                        sensors_json[key] = json_sensor

        except Exception as e:
            print(f'Failed to get sensor data , {e}')
        return sensors_json

    def __create_switch_sensor_from_json(self, motion_sensor_id, json_sensor) -> HueSwitch:
        name = json_sensor["name"]
        unique_id = json_sensor["uniqueid"]
        button_event = HueEventHelper.get_button_event_enum_from_code(json_sensor["state"]["buttonevent"])
        last_updated = json_sensor["state"]["lastupdated"]
        return HueSwitch(motion_sensor_id, unique_id, name, SensorType.SWITCH,
                         SwitchState(button_event, self.__get_timestamp_from_string(last_updated)))

    def __create_motion_sensor_from_json(self, motion_sensor_id, json_sensor) -> HueMotionSensor:
        name = json_sensor["name"]
        unique_id = json_sensor["uniqueid"]
        presence = json_sensor["state"]["presence"]
        last_updated = json_sensor["state"]["lastupdated"]

        return HueMotionSensor(motion_sensor_id, unique_id, name, SensorType.MOTION, presence,
                               self.__get_timestamp_from_string(last_updated))

    def __create_daylight_sensor_from_json(self, sensor_id, json_sensor) -> HueDayLightSensor:
        name = json_sensor["name"]
        # no id can be found
        unique_id = json_sensor["name"]
        daylight_detected = json_sensor["state"]["daylight"]
        last_updated = json_sensor["state"]["lastupdated"]

        timestamp = self.__get_timestamp_from_string(last_updated)
        sensor_state = DayLightSensorState(daylight_detected, timestamp)
        return HueDayLightSensor(sensor_id, unique_id, name, SensorType.DAYLIGHT, sensor_state)

    def __create_temperature_sensor_from_json(self, sensor_id, json_sensor) -> HueTemperatureSensor:
        name = json_sensor["name"]
        unique_id = json_sensor["uniqueid"]
        temperature = json_sensor["state"]["temperature"]
        last_updated = json_sensor["state"]["lastupdated"]

        timestamp = self.__get_timestamp_from_string(last_updated)
        sensor_state = TemperatureSensorState(temperature, timestamp)
        return HueTemperatureSensor(sensor_id, unique_id, name, SensorType.DAYLIGHT, sensor_state)

    @staticmethod
    def __get_timestamp_from_string(time_string: str, time_format: str = '%Y-%m-%dT%H:%M:%S'):
        try:
            time_object = time.strptime(time_string, time_format)
            return time.mktime(time_object)
        except Exception as e:
            print(f"Failed to convert string {time_string} to a valid timestamp {e}")

        return 0