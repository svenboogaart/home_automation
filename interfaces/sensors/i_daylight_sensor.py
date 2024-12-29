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
    def add_state(self, state: DayLightSensorState):
        pass

    @abstractmethod
    def get_state(self) -> DayLightSensorState:
        pass
