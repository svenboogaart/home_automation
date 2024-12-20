from abc import ABCMeta, abstractmethod


class IDevice(metaclass=ABCMeta):

    @abstractmethod
    def get_unique_id(self) -> str:
        pass

    @abstractmethod
    def get_name(self) -> str:
        pass
