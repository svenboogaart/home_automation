from hue.sensors.motion_sensor import MotionSensor, MOTION_SENSOR_TYPE
from hue.sensors.sensor import Sensor


def get_sensor_object_from_json(id, json_sensor) ->Sensor:
    name = json_sensor["name"]
    sensor_type = json_sensor["type"]
    match sensor_type:
        case "ZLLPresence":
            return create_motion_sensor(id, name,sensor_type, json_sensor)
        case _:
            return Sensor(id, name,sensor_type)


def create_motion_sensor(id, name, sensor_type, json_sensor) -> MotionSensor:
    return MotionSensor(id, name, sensor_type, json_sensor["state"]["presence"], json_sensor["state"]["lastupdated"])