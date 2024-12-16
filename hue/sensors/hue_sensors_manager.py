import json
from typing import List

from helpers.enums.sensor_types import SensorType
from helpers.hue_event_helper import HueEventHelper
from hue.hue_connector import HueConnector
from hue.hue_manager_abc import HueManagerAbc
from hue.sensors.hue_motion_sensor import HueMotionSensor
from hue.sensors.hue_switch import HueSwitch


class HueSensorsManager(HueManagerAbc):

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

    def get_sensor_json(self, sensor_type=None):
        sensors_json = {}
        sensor_data = self.hue_connector.run_get_request("sensors")
        if sensor_data:
            sensors_from_json = json.loads(sensor_data)
            for key, json_sensor in sensors_from_json.items():
                if sensor_type:
                    sensor_type_enum_from_json = HueEventHelper.get_sensor_enum_from_string(json_sensor["type"])
                    if sensor_type == sensor_type_enum_from_json:
                        sensors_json[key] = json_sensor
                else:
                    sensors_json[key] = json_sensor

        return sensors_json

    def __create_switch_sensor_from_json(self, motion_sensor_id, json_sensor) -> HueSwitch:
        name = json_sensor["name"]
        unique_id = json_sensor["uniqueid"]
        button_event = HueEventHelper.get_button_event_enum_from_code(json_sensor["state"]["buttonevent"])
        last_updated = json_sensor["state"]["lastupdated"]
        return HueSwitch(motion_sensor_id, unique_id, name, SensorType.SWITCH, button_event, last_updated)

    def __create_motion_sensor_from_json(self, motion_sensor_id, json_sensor) -> HueMotionSensor:
        name = json_sensor["name"]
        unique_id = json_sensor["uniqueid"]
        presence = json_sensor["state"]["presence"]
        last_updated = json_sensor["state"]["lastupdated"]
        return HueMotionSensor(motion_sensor_id, unique_id, name, SensorType.MOTION, presence, last_updated)
