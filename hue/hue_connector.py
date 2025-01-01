import json

import requests

from hue.hue_connection_settings import HueConnectionSettings
from interfaces.i_hue_connector import IHueConnector

DISCOVER_PATH = "https://discovery.meethue.com/"


class HueConnector(IHueConnector):

    def __init__(self, settings):
        self.settings = settings

    def run_put_request(self, path, data):
        try:
            full_path = self.get_full_path(path)
            request = requests.put(full_path, data, timeout=2.50)
            if request.status_code == 200:
                return request.text
            return None
        except Exception as e:
            print("exception in run_put_request")
            print(e)
            return None

    def run_get_request(self, path):
        full_path = self.get_full_path(path)
        try:
            request = requests.get(full_path, timeout=0.1)
            if request.status_code == 200:
                return request.text
            return None
        except Exception as exception:
            print(f"exception in run_get_request , {full_path}")
            print(exception)
            return None

    def run_get_request_v2(self, path):
        pass


    def get_full_path(self, path):
        return f"http://{self.settings.hue_ip_address}/api/{self.settings.hue_username}/{path}"

    def get_connection_settings(self):
        """
        [TODO] Use this method to automatically load the hue settings if not configured in the env file
        :return:
        """
        connection_data = self.run_get_request(DISCOVER_PATH)
        if connection_data:
            loaded_data = json.loads(connection_data)
            connection_id = loaded_data[0]["id"]
            internal_ipaddress = loaded_data[0]["internalipaddress"]
            port = loaded_data[0]["port"]
            print("Can connect")
            return HueConnectionSettings(connection_id, internal_ipaddress, port)

        print("Connecting to the bridge not possible.")
        return None
