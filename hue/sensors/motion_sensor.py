from hue.sensors.sensor import Sensor



class MotionSensor(Sensor):

    def __init__(self, id, unique_id, name, sensor_type, presense: str, last_update: str):
        super().__init__(id, name, sensor_type)
        self.unique_id = unique_id
        self.presense = presense
        self.last_update = last_update