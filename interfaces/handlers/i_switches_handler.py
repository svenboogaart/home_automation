from abc import ABCMeta, abstractmethod
from typing import List

from interfaces.sensors.i_switch import ISwitch


class ISwitchesHandler(metaclass=ABCMeta):

    @abstractmethod
    def update_switches(self):
        pass

    @abstractmethod
    def get_switches(self) -> List[ISwitch]:
        pass
