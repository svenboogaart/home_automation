from hue.sensors.sensor import Sensor

MOTION_SENSOR_TYPE = "ZLLPresence"

class MotionSensor(Sensor):

    def __init__(self, id, name, sensor_type, presense: str, last_update: str):
        super().__init__(id, name, sensor_type)
        self.presense = presense
        self.last_update = last_update