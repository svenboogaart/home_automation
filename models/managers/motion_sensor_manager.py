from typing import List

from hue.sensors.hue_sensors_manager import HueSensorsManager
from interfaces.sensors.i_motion_sensor import IMotionSensor


class MotionSensorManager:
    known_sensors = {}

    def __init__(self, sensor_manager: HueSensorsManager):
        self._sensor_handler = sensor_manager

    def update_sensors(self):
        for sensor in self._sensor_handler.get_motion_sensors():
            self.update_sensor(sensor)

    def get_sensors(self) -> List[IMotionSensor]:
        return list(self.known_sensors.values())

    def update_sensor(self, motion_sensor: IMotionSensor):
        if motion_sensor.get_unique_id() in self.known_sensors:
            self.known_sensors[motion_sensor.get_unique_id()].add_state(motion_sensor.get_state())
        else:
            self.known_sensors[motion_sensor.get_unique_id()] = motion_sensor

    def get_sensor(self, sensor_id: int):
        if sensor_id in self.known_sensors:
            return self.known_sensors[sensor_id]
        return None
