from abc import ABCMeta, abstractmethod
from dataclasses import dataclass

from interfaces.i_device import IDevice


@dataclass
class DayLightSensorState:
    daylight_detected: bool
    timestamp: float


class IDaylightSensor(IDevice, metaclass=ABCMeta):

    @abstractmethod
    def daylight_detected(self) -> bool:
        pass

    @abstractmethod
    def get_daylight_sensor_state(self) -> DayLightSensorState:
        pass