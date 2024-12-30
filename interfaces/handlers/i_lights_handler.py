from abc import ABCMeta, abstractmethod


class ILightsHandler(metaclass=ABCMeta):

    @abstractmethod
    def update_lights(self):
        pass

    @abstractmethod
    def get_lights(self):
        pass

    @abstractmethod
    def alarm_light(self, light_id, hue, time_pause: int = 1, number_of_flashes: int = 1, time_flash: int = 1):
        pass

    @abstractmethod
    def alarm_lights(self, hue, time_pause: int = 1, number_of_flashes: int = 1, time_flash: int = 1):
        pass

    @abstractmethod
    def get_light(self, light_id):
        pass
