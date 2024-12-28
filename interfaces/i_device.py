from abc import ABCMeta, abstractmethod


class IDevice(metaclass=ABCMeta):

    @abstractmethod
    def get_last_update_date(self) -> float:
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
