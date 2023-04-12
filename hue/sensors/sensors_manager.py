import json
from typing import List

from hue.element_manager import ElementManager
from hue.hue_connector import HueConnector
from hue.sensors.motion_sensor import MotionSensor
from hue.sensors.sensor import Sensor
from hue.sensors.sensor_factory import get_sensor_object_from_json


class SensorsManager(ElementManager):

    def __init__(self, hue_connector: HueConnector):
        super().__init__(hue_connector)

    def get_sensors(self, sensor_type = None) -> List[Sensor]:
        sensors = []
        sensor_data = self.hue_connector.run_get_request("sensors")
        if sensor_data:
            sensors_from_json = json.loads(sensor_data)
            for key, value in sensors_from_json.items():
                sensors.append(get_sensor_object_from_json(key, value))
        if sensor_type:
            sensors = [x for x in sensors if x.sensor_type == sensor_type]
        sensors.sort(key=lambda x: x.name)
        return sensors



