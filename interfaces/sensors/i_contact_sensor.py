from abc import ABCMeta, abstractmethod

from interfaces.i_device import IDevice


class IContactSensor(IDevice, metaclass=ABCMeta):

    @abstractmethod
    def has_contact(self) -> bool:
        pass

    @abstractmethod
    def get_changed_timestamp(self) -> float:
        pass
