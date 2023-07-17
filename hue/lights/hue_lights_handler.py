import json
import time
from typing import List

from database.DataLayer import DataLayer
from helpers.enums.device_state import DeviceState
from helpers.enums.hue_colors import HueColor
from hue.hue_manager_abc import HueManagerAbc
from hue.hue_connector import HueConnector
from models.lights.LightState import LightState
from models.lights.light import Light


class HueLightsHandler(HueManagerAbc):

    def __init__(self, hue_connector: HueConnector, data_layer: DataLayer):
        self.data_layer = data_layer
        super().__init__(hue_connector)

    def get_lights(self) -> List[Light]:
        lights = []
        lights_data = self.hue_connector.run_get_request("lights")
        if lights_data:
            lights_from_json = json.loads(lights_data)
            for key, value in lights_from_json.items():
                lights.append(self.create_light_object_from_json(key, value))
        return [light for light in lights if light is not None]

    def get_light(self, light_id: int) -> Light | None:
        light_data = self.hue_connector.run_get_request(f"lights/{light_id}")
        if light_data:
            light_from_json = json.loads(light_data)
            return self.create_light_object_from_json(light_id, light_from_json)
        return None

    def turn_all_lights_on(self):
        self.__set__all_light_on_state("true")

    def turn_all_lights_off(self):
        self.__set__all_light_on_state("false")

    def __set__all_light_on_state(self, state: str):
        for light in self.get_lights():
            self.set_light_on_state(light.id, state)

    def create_light_object_from_json(self, id, json_light) -> Light | None:
        try:
            name = json_light["name"]
            min_dim_level = json_light["capabilities"]["control"]["mindimlevel"]
            max_lumen = json_light["capabilities"]["control"]["maxlumen"]
            light_type = json_light["type"]
            unique_id = json_light["uniqueid"]
            state = DeviceState.OFF
            brightness, hue, saturation = "", "", "'"
            if json_light["state"]["on"]:
                state = DeviceState.ON
                try:
                    brightness = json_light["state"]["bri"]
                    hue = json_light["state"]["hue"]
                    saturation = json_light["state"]["sat"]
                except:
                    hue = "0"
                    brightness = "0"
                    saturation = "0"

            return Light(id, unique_id, name, min_dim_level, max_lumen, light_type, brightness, hue, saturation, state)
        except Exception as e:
            # print(e)
            return None

    def set_light_on_state(self, light_id: int, state: str) -> str:
        return self.hue_connector.run_put_request("lights/%s/state" % light_id, "{\"on\": %s}" % state)

    def set_light_state(self, light_id: str, new_state: LightState) -> str:
        data = {"on": new_state.device_state == DeviceState.ON, "hue": new_state.hue, "bri": new_state.brightness,
                "sat": new_state.saturation}
        return self.hue_connector.run_put_request("lights/%s/state" % light_id, json.dumps(data))

    def alarm_light(self, light_id, time_flash, time_pause, number_of_flashes, hue=HueColor.RED):
        light = self.get_light(light_id)
        current_state = light.light_state
        on_state = LightState(100, hue, current_state.saturation, DeviceState.ON)
        off_state = LightState(current_state.brightness, hue, current_state.saturation, DeviceState.OFF)
        for x in range(number_of_flashes):
            print(self.set_light_state(light.id, on_state))
            time.sleep(time_flash)
            self.set_light_state(light.id, off_state)
            time.sleep(time_pause)

        self.set_light_state(light.id, current_state)
