from abc import ABCMeta, abstractmethod

from interfaces.i_device import IDevice


class ISwitch(IDevice, metaclass=ABCMeta):

    @abstractmethod
    def state_changed(self):
        pass

    @abstractmethod
    def is_release_long_click(self):
        pass

    @abstractmethod
    def is_pressed_event(self):
        pass

    @abstractmethod
    def is_released_event(self):
        pass

    @abstractmethod
    def is_hold_event(self):
        pass

    @abstractmethod
    def get_last_update_date(self):
        pass

    @abstractmethod
    def button_off_used(self) -> bool:
        pass

    @abstractmethod
    def button_on_used(self) -> bool:
        pass
