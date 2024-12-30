from typing import List

from hue.data_loader.hue_sensors_loader import HueSensorsLoader
from hue.sensors.hue_temperature_sensor import HueTemperatureSensor
from interfaces.handlers.i_temperature_sensor_handler import ITemperatureSensorHandler


class HueTemperatureSensorHandler(ITemperatureSensorHandler):

    def __init__(self, hue_sensor_loader: HueSensorsLoader):
        self._known_sensors: dict[str, HueTemperatureSensor] = {}
        self._hue_sensor_loader = hue_sensor_loader

    def update_temperature_sensors(self):
        for sensor in self._hue_sensor_loader.get_temperature_sensors():
            self.update_sensor(sensor)

    def get_temperature_sensors(self) -> List[HueTemperatureSensor]:
        return list(self._known_sensors.values())

    def update_sensor(self, sensor: HueTemperatureSensor):
        if sensor.get_unique_id() in self._known_sensors:
            self._known_sensors[sensor.get_unique_id()].add_state(sensor.get_state())
        else:
            self._known_sensors[sensor.get_unique_id()] = sensor
