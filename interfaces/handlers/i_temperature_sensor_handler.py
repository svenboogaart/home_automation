from abc import ABCMeta, abstractmethod
from typing import List

from interfaces.sensors.i_temperature_sensor import ITemperatureSensor


class ITemperatureSensorHandler(metaclass=ABCMeta):

    @abstractmethod
    def update_temperature_sensors(self):
        pass

    @abstractmethod
    def get_temperature_sensors(self) -> List[ITemperatureSensor]:
        pass
