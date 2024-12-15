from abc import ABCMeta, abstractmethod
from models.lights.LightState import LightState


class ILight(metaclass=ABCMeta):

    @abstractmethod
    def add_state(self, state: LightState):
        pass

    @abstractmethod
    def state_changed(self):
        pass

    @abstractmethod
    def get_unique_id(self) -> str:
        pass

    @abstractmethod
    def get_name(self) -> str:
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
