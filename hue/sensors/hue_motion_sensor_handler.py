from typing import List

from hue.sensors.hue_motion_sensor import HueMotionSensor
from hue.sensors.hue_sensors_manager import HueSensorsManager
from interfaces.handlers.i_motion_sensor_handler import IMotionSensorHandler


class HueMotionSensorHandler(IMotionSensorHandler):

    def __init__(self, hue_sensor_manager: HueSensorsManager):
        self._known_motion_sensor: dict[str, HueMotionSensor] = {}
        self._hue_sensor_manager = hue_sensor_manager

    def update_motion_sensors(self):
        for motion_sensor in self._hue_sensor_manager.get_motion_sensors():
            self.update_motion_sensor(motion_sensor)

    def get_motion_sensor(self) -> List[HueMotionSensor]:
        return list(self._known_motion_sensor.values())

    def update_motion_sensor(self, motion_sensor: HueMotionSensor):

        if motion_sensor.get_unique_id() in self._known_motion_sensor:
            self._known_motion_sensor[motion_sensor.get_unique_id()].add_state(motion_sensor.get_state())
        else:
            self._known_motion_sensor[motion_sensor.get_unique_id()] = motion_sensor
