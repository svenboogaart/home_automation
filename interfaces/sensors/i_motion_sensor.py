from abc import ABCMeta, abstractmethod
from dataclasses import dataclass

from interfaces.i_device import IDevice


@dataclass
class MotionSensorState:
    presence: bool
    last_updated: float

    def __eq__(self, other):
        if not isinstance(other, MotionSensorState):
            return NotImplemented
        return self.presence == other.presence and self.last_updated == other.last_updated


class IMotionSensor(IDevice, metaclass=ABCMeta):

    @abstractmethod
    def motion_detected(self):
        pass

    @abstractmethod
    def add_state(self, state: MotionSensorState):
        pass

    @abstractmethod
    def get_state(self) -> MotionSensorState:
        pass

    @abstractmethod
    def new_motion_detected(self):
        pass
