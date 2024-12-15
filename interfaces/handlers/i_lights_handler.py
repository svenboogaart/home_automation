from abc import ABCMeta, abstractmethod

from models.lights.LightState import LightState


class ILightsHandler(metaclass=ABCMeta):

    @abstractmethod
    def update_lights(self):
        pass

    @abstractmethod
    def get_lights(self):
        pass

    @abstractmethod
    def alarm_light(self, light_id, time_flash, time_pause, number_of_flashes, hue):
        pass


    @abstractmethod
    def get_light(self, id):
        pass
