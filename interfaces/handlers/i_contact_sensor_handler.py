from abc import ABCMeta, abstractmethod
from typing import List

from interfaces.sensors.i_contact_sensor import IContactSensor


class IContactSensorHandler(metaclass=ABCMeta):

    @abstractmethod
    def update_contact_sensors(self):
        pass

    @abstractmethod
    def get_contact_sensors(self) -> List[IContactSensor]:
        pass
