from helpers.enums.hue_dimmer_event import HueDimmerEvent
from helpers.enums.sensor_types import SensorType


class HueEventHelper:

    @staticmethod
    def get_button_event_enum_from_code(value):
        return HueDimmerEvent(value) if value in HueDimmerEvent._value2member_map_ else None

    @staticmethod
    def get_sensor_enum_from_string(value):
        return SensorType(value) if value in SensorType._value2member_map_ else None


