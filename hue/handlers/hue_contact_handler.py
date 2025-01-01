from typing import List

from hue.data_loader.api_v2.hue_contact_loader import HueContactLoaderV2
from hue.sensors.hue_contact_sensor import HueContactSensor
from interfaces.handlers.i_contact_sensor_handler import IContactSensorHandler
from interfaces.sensors.i_contact_sensor import IContactSensor


class HueContactHandler(IContactSensorHandler):

    def __init__(self, hue_contact_loader: HueContactLoaderV2):
        self._known_sensors: dict[str, HueContactSensor] = {}
        self._hue_contact_loader = hue_contact_loader

    def update_contact_sensors(self):
        for sensor in self._hue_contact_loader.get_contact_sensors():
            self._update_sensor(sensor)

    def get_contact_sensors(self) -> List[IContactSensor]:
        return list(self._known_sensors.values())

    def _update_sensor(self, sensor: HueContactSensor):
        if sensor.get_unique_id() in self._known_sensors:
            self._known_sensors[sensor.get_unique_id()].add_state(sensor.get_state())
        else:
            self._known_sensors[sensor.get_unique_id()] = sensor
