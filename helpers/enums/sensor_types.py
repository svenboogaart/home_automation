from enum import Enum


class SensorType(Enum):
    MOTION = "ZLLPresence"
    DAYLIGHT = "Daylight"
    SWITCH = "ZLLSwitch"
    TEMPERATURE = "ZLLTemperature"
    CONTACT = "contact"
