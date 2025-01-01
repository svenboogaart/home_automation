import json

import requests

from hue.hue_connection_settings import HueConnectionSettings
from interfaces.i_hue_connector import IHueConnector
from settings.settings import Settings

DISCOVER_PATH = "https://discovery.meethue.com/"

# Suppress the warning
import urllib3
from urllib3.exceptions import InsecureRequestWarning

# Suppress the warning
urllib3.disable_warnings(InsecureRequestWarning)


class HueConnectorV2(IHueConnector):

    def __init__(self, settings: Settings):
        self.settings = settings
        self.hue_ip_address = settings.hue_ip_address
        self.oauth_token = settings.hue_api_v2_username
        self.base_url = f"https://{self.hue_ip_address}/clip/v2/resource/"

    def run_get_request(self, path):
        full_path = self.get_full_path(path)
        try:
            # Headers with OAuth token for authentication
            headers = {
                'Accept': 'application/json',
                "hue-application-key": f'{self.oauth_token}'
            }
            # Timeout is kept the same
            request = requests.get(full_path, headers=headers, timeout=0.5, verify=False)

            # Check for a successful response
            if request.status_code == 200:
                return request.json()  # In v2, data is usually returned as JSON
            return None
        except Exception as exception:
            print(f"Exception in run_get_request v2, {full_path}")
            print(exception)
            return None

    def get_full_path(self, path):
        # Constructing the full path for v2 (no username in URL)
        return f"{self.base_url}{path}"

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
