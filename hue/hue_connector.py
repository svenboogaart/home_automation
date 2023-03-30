import json

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
        self.get_lights()


    def get_lights(self):
        lights = []
        lights_request = requests.get(self.create_url("lights"))
        if(lights_request.status_code == 200):
            lights_from_json = json.loads(lights_request.text)
            lights = []
            for key, value in lights_from_json.items():
                lights.append(self.create_light_object_from_json(key,value))
            return lights
        return lights

    def create_url(self, path):
        return f"{self.settings.hue_ip_address}/api/{self.settings.hue_username}/{path}"


    def create_light_object_from_json(self, id, json_light):
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



    def get_connection_settings(self):
        connection_request = requests.get(DISCOVER_PATH, timeout=2.50)
        if (connection_request.status_code == 200):
            loaded_data = json.loads(connection_request.text)
            id = loaded_data[0]["id"]
            internalipaddress = loaded_data[0]["internalipaddress"]
            port = loaded_data[0]["port"]
            print("Can connect")
            return ConnectionSettings(id, internalipaddress, port)
        else:
            print("Connecting to the bridge not possible.")
            return None