from typing import List

from interfaces.handlers.i_motion_sensor_handler import IMotionSensorHandler
from interfaces.sensors.i_motion_sensor import IMotionSensor


class MotionSensorManager:

    def __init__(self, sensor_handler: IMotionSensorHandler):
        self._motion_sensor_handler = sensor_handler

    def update_motion_sensors(self):
        self._motion_sensor_handler.update_motion_sensors()

    def get_motion_sensors(self) -> List[IMotionSensor]:
        return self._motion_sensor_handler.get_motion_sensors()
