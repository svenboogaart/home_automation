from threading import Thread
from typing import List

from helpers.enums.hue_colors import HueColor
from hue.lights.hue_lights_handler import HueLightsHandler
from models.lights.light import Light


class LightsManager:
    known_lights = {}

    def __init__(self, lights_handler: HueLightsHandler):
        # TODO make interface for HueLightsHandler
        self._lights_handler = lights_handler

    def update_lights(self):
        for light in self._lights_handler.get_lights():
            self.update_light(light)

    def get_lights(self) -> List[Light]:
        return list(self.known_lights.values())

    def update_light(self, light: Light):
        if light.unique_id in self.known_lights:
            self.known_lights[light.unique_id].add_state(light.light_state)
        else:
            self.known_lights[light.unique_id] = light

    def alarm_lights(self, time_flash, time_pause, number_of_flashes):
        for light in self._lights_handler.get_lights():
            self._lights_handler.alarm_light(light.id, time_flash, time_pause, number_of_flashes)

    def alarm_light(self, light_id, time_flash, time_pause, number_of_flashes, color: HueColor = HueColor.RED):
        Thread(target=self._lights_handler.alarm_light, args=(light_id, time_flash, time_pause, number_of_flashes, color)).start()

    def get_light(self, id: int):
        if id in self.known_lights:
            return self.known_lights[id]
        return None
