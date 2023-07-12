from enum import Enum


class DeviceState(Enum):
    UNKNOWN = 1
    STAND_BY = 2
    ON = 3
    OFF = 4