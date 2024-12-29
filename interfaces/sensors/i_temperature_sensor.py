from abc import ABCMeta, abstractmethod
from dataclasses import dataclass

from interfaces.i_device import IDevice


@dataclass
class TemperatureSensorState:
    temperature: float
    timestamp: float


class ITemperatureSensor(IDevice, metaclass=ABCMeta):

    @abstractmethod
    def get_state(self) -> TemperatureSensorState:
        pass

    @abstractmethod
    def get_temperature(self) -> float:
        pass
