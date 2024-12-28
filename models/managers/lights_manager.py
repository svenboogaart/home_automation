from typing import List

from helpers.enums.hue_colors import HueColor
from interfaces.handlers.i_lights_handler import ILightsHandler
from interfaces.lights.i_light import ILight


class LightsManager:
    def __init__(self, lights_handler: ILightsHandler):
        self._lights_handler = lights_handler

    def update_lights(self):
        self._lights_handler.update_lights()

    def get_lights(self) -> List[ILight]:
        return self._lights_handler.get_lights()

    def alarm_lights(self, time_flash, time_pause, number_of_flashes):
        for light in self._lights_handler.get_lights():
            self.alarm_light(light.id, time_flash, time_pause, number_of_flashes)

    def alarm_light(self, light_id, time_flash, time_pause, number_of_flashes, color: HueColor = HueColor.RED):
        self._lights_handler.alarm_light(light_id, time_flash, time_pause, number_of_flashes, color)

    def get_light(self, light_id: int):
        self._lights_handler.get_light(light_id)
