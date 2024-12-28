import json
import threading
import time
from typing import List

from database.data_layer import DataLayer
from helpers.enums.device_state import DeviceState
from hue.hue_connector import HueConnector
from hue.hue_manager_abc import HueManagerAbc
from hue.lights.hue_light import HueLight
from interfaces.handlers.i_lights_handler import ILightsHandler
from models.lights.light_state import LightState


class HueLightsHandler(HueManagerAbc, ILightsHandler):

    def __init__(self, hue_connector: HueConnector, data_layer: DataLayer):
        self.data_layer = data_layer
        super().__init__(hue_connector)
        self.known_lights = {}

    def update_lights(self):
        for light in self.get_lights_from_manager():
            self.update_light(light)

    def update_light(self, light: HueLight):
        if light.get_unique_id() in self.known_lights:
            self.known_lights[light.get_unique_id()].add_state(light.light_state)
        else:
            self.known_lights[light.unique_id] = light

    def get_lights(self) -> List[HueLight]:
        return list(self.known_lights.values())

    def get_lights_from_manager(self) -> List[HueLight]:
        lights: List[HueLight] = []
        lights_data = self.hue_connector.run_get_request("lights")
        if lights_data:
            lights_from_json = json.loads(lights_data)
            for key, value in lights_from_json.items():
                lights.append(self.create_light_object_from_json(key, value))
        return [light for light in lights if light is not None]

    def get_light(self, light_id: int) -> HueLight | None:
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

    @staticmethod
    def create_light_object_from_json(light_id, json_light) -> HueLight | None:
        try:
            name = json_light["name"]
            min_dim_level = json_light["capabilities"]["control"]["mindimlevel"]
            max_lumen = json_light["capabilities"]["control"]["maxlumen"]
            light_type = json_light["type"]
            unique_id = json_light["uniqueid"]
            state = DeviceState.OFF
            brightness, hue, saturation = "", "", "'"
            if json_light["state"]["on"]:

                try:
                    brightness = json_light["state"]["bri"]
                except KeyError as e:
                    print(f"Missing brightness: {e}")
                    brightness = "0"  # Default value

                try:
                    light_type = json_light["type"]
                    if light_type == 'Extended color light':
                        hue = json_light["state"]["hue"]
                        saturation = json_light["state"]["sat"]
                    elif light_type == 'Color temperature light':
                        pass
                    else:
                        print(f"no method available for lights of type: {type}")

                except KeyError as e:
                    print(f"Failed to load data: {e}")
                    brightness = "0"  # Default value
                    hue = 0
                    saturation = 0

            return HueLight(light_id, unique_id, name, min_dim_level, max_lumen, light_type,
                            LightState(brightness, hue, saturation, state), time.time())
        except Exception as e:
            print("Failed to create light object from json. ", e)
            # print(e)
            return None

    def set_light_on_state(self, light_id: int, state: str) -> str:
        return self.hue_connector.run_put_request(f"lights/{light_id}/state", "{\"on\": %s}" % state)

    def set_light_state(self, light_id: str, new_state: LightState) -> str:
        data = {"on": new_state.device_state == DeviceState.ON, "hue": new_state.hue, "bri": new_state.brightness,
                "sat": new_state.saturation}
        return self.hue_connector.run_put_request(f"lights/{light_id}/state", json.dumps(data))

    def alarm_light(self, light_id, hue, time_pause: int = 1, number_of_flashes: int = 1, time_flash: int = 1):
        def flash_light():
            light = self.get_light(light_id)
            current_state = light.light_state
            on_state = LightState(100, hue, current_state.saturation, DeviceState.ON)
            off_state = LightState(current_state.brightness, hue, current_state.saturation, DeviceState.OFF)

            for _ in range(number_of_flashes):
                self.set_light_state(light.id, on_state)
                time.sleep(time_flash)
                self.set_light_state(light.id, off_state)
                time.sleep(time_pause)

            self.set_light_state(light.id, current_state)

        # Start the flash_light function in a separate thread
        threading.Thread(target=flash_light).start()

