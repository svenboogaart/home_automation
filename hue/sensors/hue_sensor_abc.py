from helpers.enums.sensor_types import SensorType


# pylint: disable=R0903


class HueSensorABC:

    def __init__(self, sensor_id: int, name: str, sensor_type: SensorType):
        self.id = sensor_id
        self.name = name
        self.sensor_type = sensor_type
