from abc import ABCMeta, abstractmethod
from typing import List

from interfaces.sensors.i_daylight_sensor import IDaylightSensor


class IDaylightSensorHandler(metaclass=ABCMeta):

    @abstractmethod
    def update_daylight_sensors(self):
        pass

    @abstractmethod
    def get_daylight_sensors(self) -> List[IDaylightSensor]:
        pass
