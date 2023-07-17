from typing import List

from hue.sensors.hue_sensors_manager import HueSensorsManager
from models.sensors.motion_sensor import MotionSensor


class MotionSensorManager:
    known_sensors = {}

    def __init__(self, sensor_manager: HueSensorsManager):
        # TODO make interface for HueLightsHandler
        self._sensor_handler = sensor_manager

    def update_sensors(self):
        for sensor in self._sensor_handler.get_motion_sensors():
            self.update_sensor(sensor)

    def get_sensors(self) -> List[MotionSensor]:
        return list(self.known_sensors.values())

    def update_sensor(self, switch: MotionSensor):
        if switch.unique_id in self.known_sensors:
            self.known_sensors[switch.unique_id].add_state(switch.state)
        else:
            self.known_sensors[switch.unique_id] = switch

    def get_sensor(self, id: int):
        if id in self.known_sensors:
            return self.known_sensors[id]
        return None
