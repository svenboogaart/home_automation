import json
from typing import List

import requests as requests

from enums.device_state import DeviceState
from hue.connection_settings import ConnectionSettings
from hue.light import Light
from settings.settings import Settings

DISCOVER_PATH = "https://discovery.meethue.com/"


class HueConnector:

    def connect(self):
        print("connecting")
        self.settings = Settings()
        self.lights = self.get_lights()

    def get_lights(self) -> List[Light]:
        lights = []
        lights_data = self.run_get_request("lights")
        if lights_data:
            lights_from_json = json.loads(lights_data)
            lights = []
            for key, value in lights_from_json.items():
                lights.append(self.create_light_object_from_json(key, value))
                self.set_light_on_state(lights.pop().id, "false")
            return lights
        return lights

    def create_light_object_from_json(self, id, json_light) -> Light:
        try:
            name = json_light["name"]
            min_dim_level = json_light["capabilities"]["control"]["mindimlevel"]
            max_lumen = json_light["capabilities"]["control"]["maxlumen"]
            light_type = json_light["type"]
            state = DeviceState.OFF
            if json_light["state"]["on"] == True:
                state = DeviceState.ON

            return Light(id, name, min_dim_level, max_lumen, light_type, state)
        except Exception as e:
            print(e)
            return None

    def set_light_on_state(self, light_id: int, state: str) -> str:
        return self.run_put_request("lights/%s/state" % light_id, "{\"on\": %s}" % state)

    def run_put_request(self, path, data):
        full_path = self.get_full_path(path)
        request = requests.put(full_path, data, timeout=2.50)
        if request.status_code == 200:
            return request.text
        else:
            return None

    def run_get_request(self, path):
        full_path = self.get_full_path(path)
        request = requests.get(full_path, timeout=2.50)
        if request.status_code == 200:
            return request.text
        else:
            return None

    def get_full_path(self, path):
        return f"{self.settings.hue_ip_address}/api/{self.settings.hue_username}/{path}"

    def get_connection_settings(self):
        """
        [TODO] automatically load the hue settings if not configured in the env file
        :return:
        """
        connection_data = self.run_get_request(DISCOVER_PATH)
        if (connection_data):
            loaded_data = json.loads(connection_data)
            id = loaded_data[0]["id"]
            internalipaddress = loaded_data[0]["internalipaddress"]
            port = loaded_data[0]["port"]
            print("Can connect")
            return ConnectionSettings(id, internalipaddress, port)
        else:
            print("Connecting to the bridge not possible.")
            return None
