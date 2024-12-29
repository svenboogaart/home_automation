from abc import ABCMeta, abstractmethod

from interfaces.i_device import IDevice
from models.lights.light_state import LightState


class ILight(IDevice, metaclass=ABCMeta):

    @abstractmethod
    def add_state(self, state: LightState):
        pass

    @abstractmethod
    def get_type(self) -> str:
        pass

    @abstractmethod
    def get_light_state(self) -> LightState:
        pass

    @abstractmethod
    def get_previous_light_state(self) -> LightState:
        pass
