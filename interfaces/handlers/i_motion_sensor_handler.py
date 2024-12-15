from abc import ABCMeta, abstractmethod
from typing import List

from interfaces.sensors.i_switch import ISwitch


class IMotionSensorHandler(metaclass=ABCMeta):

    @abstractmethod
    def update_motion_sensors(self):
        pass

    @abstractmethod
    def get_motion_sensor(self) -> List[ISwitch]:
        pass

