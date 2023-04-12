import json
from typing import List

from enums.device_state import DeviceState
from hue.element_manager import ElementManager
from hue.hue_connector import HueConnector
from hue.lights.light import Light


class LightsManager(ElementManager):

    def __init__(self, hue_connector: HueConnector):
        super().__init__(hue_connector)



    def get_lights(self) -> List[Light]:
        lights = []
        lights_data = self.hue_connector.run_get_request("lights")
        if lights_data:
            lights_from_json = json.loads(lights_data)
            for key, value in lights_from_json.items():
                lights.append(self.create_light_object_from_json(key, value))
        return lights

    def turn_all_lights_on(self):
        self.__set__all_light_on_state("true")


    def turn_all_lights_off(self):
        self.__set__all_light_on_state("false")

    def __set__all_light_on_state(self, state: str):
        for light in self.get_lights():
            self.set_light_on_state(light.id, state)

    def create_light_object_from_json(self, id, json_light) -> Light:
        name = json_light["name"]
        min_dim_level = json_light["capabilities"]["control"]["mindimlevel"]
        max_lumen = json_light["capabilities"]["control"]["maxlumen"]
        light_type = json_light["type"]
        state = DeviceState.OFF
        if json_light["state"]["on"] == True:
            state = DeviceState.ON

        return Light(id, name, min_dim_level, max_lumen, light_type, state)

    def set_light_on_state(self, light_id: int, state: str) -> str:
        return self.run_put_request("lights/%s/state" % light_id, "{\"on\": %s}" % state)
