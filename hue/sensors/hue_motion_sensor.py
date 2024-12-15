from typing import List

from interfaces.sensors.i_motion_sensor import IMotionSensor, MotionSensorState
from models.sensors.sensor import Sensor


class HueMotionSensor(Sensor, IMotionSensor):

    def __init__(self, id, unique_id, name, sensor_type, presence: bool, last_update: str):
        super().__init__(id, name, sensor_type)
        self.unique_id = unique_id
        self.state = MotionSensorState(presence, last_update)
        self.last_states: List[MotionSensorState] = []

    def add_state(self, state: MotionSensorState):
        self.last_states.append(state)
        self.state = state

    def state_changed(self):
        if len(self.last_states) < 2:
            return True
        try:
            return self.last_states[-1] != self.last_states[-2]
        except IndexError:
            return False

    def motion_detected(self):
        return len(self.last_states) > 0 and self.last_states[-1] is not None and self.last_states[-1].presence

    def get_unique_id(self):
        return self.unique_id

    def get_last_update_date(self):
        return len(self.last_states) > 0 and self.last_states[-1] is not None and self.last_states[-1].last_updated

    def get_name(self):
        return self.name

    def get_state(self) -> MotionSensorState:
        try:
            return self.last_states[-1]
        except IndexError:
            return None
