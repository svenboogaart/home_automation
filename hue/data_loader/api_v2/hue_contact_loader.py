import time
from datetime import datetime
from typing import List

from hue.hue_connector_v2 import HueConnectorV2
from hue.hue_data_loader_abc import HueDataLoaderAbc
from hue.sensors.hue_contact_sensor import HueContactSensor, ContactState


# pylint: disable=W0246
class HueContactLoaderV2(HueDataLoaderAbc):

    def __init__(self, hue_connector: HueConnectorV2):
        super().__init__(hue_connector)

    def get_contact_sensors(self) -> List[HueContactSensor]:
        try:
            hue_contacts = []

            sensor_data = self.hue_connector.run_get_request('contact')
            if sensor_data:
                for item in sensor_data['data']:
                    sensor_id = item['id']
                    changed_timestamp = self.__get_timestamp_from_string(item['contact_report']['changed'])
                    has_contact = item['contact_report']['state'] == 'contact'
                    owner = item['owner']['rid']
                    try:
                        single_sensor = self.hue_connector.run_get_request(f'device/{owner}')

                        name = single_sensor['data'][0]['metadata']['name']
                    except Exception as load_single_sensor_exception:
                        print(f"failed to find sensor data for {sensor_id}, exception {load_single_sensor_exception}")
                        name = sensor_id
                    hue_contacts.append(
                        HueContactSensor(sensor_id, sensor_id, name,
                                         ContactState(has_contact, changed_timestamp, time.time())))
            return hue_contacts

        except Exception as e:
            print(f'Failed to load the contact sensors, exception {e}')
            return []

    @staticmethod
    def __get_timestamp_from_string(time_string: str) -> time:

        # Remove the 'Z' from the string (it stands for UTC)
        time_string = time_string.rstrip('Z')

        # Convert the string to a datetime object
        dt = datetime.fromisoformat(time_string)

        # Convert datetime to a struct_time object (timezone-unaware)
        struct_time = dt.timetuple()

        # Convert struct_time to a UNIX timestamp (seconds since epoch)
        timestamp = time.mktime(struct_time)

        return timestamp
