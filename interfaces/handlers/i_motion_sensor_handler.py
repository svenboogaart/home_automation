from abc import ABCMeta, abstractmethod
from typing import List

from hue.sensors.hue_motion_sensor import HueMotionSensor


class IMotionSensorHandler(metaclass=ABCMeta):

    @abstractmethod
    def update_motion_sensors(self):
        pass

    @abstractmethod
    def get_motion_sensors(self) -> List[HueMotionSensor]:
        pass
