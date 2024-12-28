from helpers.enums.hue_dimmer_event import HueDimmerEvent
from helpers.enums.sensor_types import SensorType


class HueEventHelper:

    @staticmethod
    def get_button_event_enum_from_code(value: str):
        for dimmer_event in HueDimmerEvent:
            if dimmer_event.value == value:
                return dimmer_event
        return None

    @staticmethod
    def get_sensor_enum_from_string(value: str):
        for sensor in SensorType:
            if sensor.value == value:
                return sensor
        return None
