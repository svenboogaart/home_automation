import json
from typing import List

from helpers.constants import SensorTypes
from hue.element_manager import ElementManager
from hue.hue_connector import HueConnector
from hue.sensors.motion_sensor import MotionSensor
from hue.sensors.sensor import Sensor
from hue.sensors.switch import Switch


class HueSensorsManager(ElementManager):

    def __init__(self, hue_connector: HueConnector):
        super().__init__(hue_connector)

    def get_switches(self) -> List[Switch]:
        switches = []
        for index, switch_data in self.get_sensor_json(SensorTypes.SWITCH).items():
            switches.append(self.__create_switch_sensor_from_json(index, switch_data))
        return switches

    def get_sensor_json(self, sensor_type=None):
        sensors_json = {}
        sensor_data = self.hue_connector.run_get_request("sensors")
        if sensor_data:
            sensors_from_json = json.loads(sensor_data)
            for key, json_sensor in sensors_from_json.items():
                if (sensor_type):
                    sensor_type_from_json = json_sensor["type"]
                    if sensor_type == sensor_type_from_json:
                        sensors_json[key] = json_sensor
                else:
                    sensors_json[key] = json_sensor

        return sensors_json

    def __create_switch_sensor_from_json(self, id, json_sensor) -> Switch:
        name = json_sensor["name"]
        unique_id = json_sensor["uniqueid"]
        button_event = json_sensor["state"]["buttonevent"]
        last_updated = json_sensor["state"]["lastupdated"]
        return Switch(id, unique_id, name, SensorTypes.SWITCH, button_event, last_updated)
