from helpers.enums.sensor_types import SensorType
from hue.sensors.sensor_abc import SensorABC


# pylint: disable=R0903


class DayLightSensor(SensorABC):

    def __init__(self, sensor_id: int, name: str, sensor_type: SensorType, daylight: bool, last_update: str):
        super().__init__(sensor_id, name, sensor_type)
        self._daylight = daylight
        self.last_update = last_update

    def daylight_started(self):
        return self._daylight
