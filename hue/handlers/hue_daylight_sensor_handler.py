from typing import List

from hue.data_loader.hue_sensors_loader import HueSensorsLoader
from hue.sensors.hue_daylight_sensor import HueDayLightSensor
from interfaces.handlers.i_daylight_sensor_handler import IDaylightSensorHandler


class HueDaylightSensorHandler(IDaylightSensorHandler):

    def __init__(self, hue_sensor_loader: HueSensorsLoader):
        self._known_daylight_sensors: dict[str, HueDayLightSensor] = {}
        self._hue_sensor_loader = hue_sensor_loader

    def get_daylight_sensors(self) -> List[HueDayLightSensor]:
        return list(self._known_daylight_sensors.values())

    def update_daylight_sensors(self):
        for daylight_sensor in self._hue_sensor_loader.get_daylight_sensors():
            self.update_daylight_sensor(daylight_sensor)

    def update_daylight_sensor(self, daylight_sensor: HueDayLightSensor):
        if daylight_sensor.get_unique_id() in self._known_daylight_sensors:
            self._known_daylight_sensors[daylight_sensor.get_unique_id()].add_state(daylight_sensor.get_state())
        else:
            self._known_daylight_sensors[daylight_sensor.get_unique_id()] = daylight_sensor
