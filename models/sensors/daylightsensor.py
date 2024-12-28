from dataclasses import dataclass

from models.sensors.sensor_abc import SensorABC


@dataclass
class DayLightSensor(SensorABC):
    daylight: bool
    last_update: str

    def __init__(self, sensor_id, name, sensor_type, daylight: bool, last_update: str):
        super().__init__(sensor_id, name, sensor_type)
        self.daylight = daylight
        self.last_update = last_update
