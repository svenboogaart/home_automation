from abc import ABC


# pylint: disable=R0903

class SensorABC(ABC):

    def __init__(self, sensor_id, name, sensor_type):
        self.id = sensor_id
        self.name = name
        self.sensor_type = sensor_type
