import json

import requests as requests

from hue.connection_settings import ConnectionSettings
from settings.settings import Settings

DISCOVER_PATH = "https://discovery.meethue.com/"


class HueConnector:

    def __init__(self, settings):
        self.settings = settings

    def run_put_request(self, path, data):
        try:
            full_path = self.get_full_path(path)
            request = requests.put(full_path, data, timeout=2.50)
            if request.status_code == 200:
                return request.text
            else:
                return None
        except Exception as e:
            print("exception")
            print(e)
            return None

    def run_get_request(self, path):
        try:
            full_path = self.get_full_path(path)
            request = requests.get(full_path, timeout=2.50)
            if request.status_code == 200:
                return request.text
            else:
                return None
        except Exception as exception:
            print("exception")
            print(exception)
            return None

    def get_full_path(self, path):
        return f"{self.settings.hue_ip_address}/api/{self.settings.hue_username}/{path}"

    def get_connection_settings(self):
        """
        [TODO] Use this method to automatically load the hue settings if not configured in the env file
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


