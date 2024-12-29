from typing import List

from hue.sensors.hue_sensor_abc import HueSensorABC
from interfaces.sensors.i_motion_sensor import IMotionSensor, MotionSensorState


# pylint: disable=R0801

class HueMotionSensor(HueSensorABC, IMotionSensor):

    def __init__(self, sensor_id, unique_id, name, sensor_type, presence: bool, last_update: float):
        super().__init__(sensor_id, name, sensor_type)
        self.unique_id = unique_id
        self.state = MotionSensorState(presence, last_update)
        self.last_states: List[MotionSensorState] = [self.state]

    def add_state(self, state: MotionSensorState):
        if len(self.last_states) > 500:
            del self.last_states[0]
        self.last_states.append(state)
        self.state = state

    def state_changed(self):
        if len(self.last_states) < 2:
            return True
        return self.last_states[-1] != self.last_states[-2]

    def motion_detected(self):
        return len(self.last_states) > 0 and self.last_states[-1] is not None and self.last_states[-1].presence

    def new_motion_detected(self):
        if len(self.last_states) <= 1:
            return False

        current_state = self.last_states[-1]
        previous_state = self.last_states[-2]

        if current_state is None or previous_state is None:
            return False

        return current_state.presence and not previous_state.presence

    def get_unique_id(self):
        return self.unique_id

    def get_last_update_date(self) -> float:
        if len(self.last_states) == 0:
            return 0
        return self.last_states[-1].last_updated

    def get_name(self):
        return self.name

    def get_state(self) -> MotionSensorState | None:
        try:
            return self.last_states[-1]
        except IndexError:
            return None
