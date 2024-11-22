from hue.sensors.sensor import Sensor


class DayLightSensor(Sensor):

    def __init__(self, id, name, sensor_type, daylight: bool, last_update: str):
        super().__init__(id, name, sensor_type)
        self.daylight = daylight
        self.last_update = last_update
