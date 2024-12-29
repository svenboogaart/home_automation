from typing import List

from hue.data_loader.hue_sensors_loader import HueSensorsLoader
from hue.sensors.hue_motion_sensor import HueMotionSensor
from interfaces.handlers.i_motion_sensor_handler import IMotionSensorHandler


class HueMotionSensorHandler(IMotionSensorHandler):

    def __init__(self, hue_sensor_loader: HueSensorsLoader):
        self._known_motion_sensor: dict[str, HueMotionSensor] = {}
        self._hue_sensor_loader = hue_sensor_loader

    def update_motion_sensors(self):
        for motion_sensor in self._hue_sensor_loader.get_motion_sensors():
            self.update_motion_sensor(motion_sensor)

    def get_motion_sensors(self) -> List[HueMotionSensor]:
        return list(self._known_motion_sensor.values())

    def update_motion_sensor(self, motion_sensor: HueMotionSensor):
        if motion_sensor.get_unique_id() in self._known_motion_sensor:
            self._known_motion_sensor[motion_sensor.get_unique_id()].add_state(motion_sensor.get_state())
        else:
            self._known_motion_sensor[motion_sensor.get_unique_id()] = motion_sensor
