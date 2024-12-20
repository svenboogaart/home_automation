from abc import ABCMeta, abstractmethod


class ISwitch(metaclass=ABCMeta):

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
    def get_unique_id(self):
        pass

    @abstractmethod
    def get_last_update_date(self):
        pass

    def get_name(self):
        pass

    @abstractmethod
    def button_off_used(self) -> bool:
        pass

    @abstractmethod
    def button_on_used(self) -> bool:
        pass
