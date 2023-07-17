from models.sensors.sensor import Sensor


class MotionSensorState:

    def __init__(self, presence: bool, last_updated):
        self.presence = presence
        self.last_updated = last_updated

    def __eq__(self, other):
        if not isinstance(other, MotionSensorState):
            # don't attempt to compare against unrelated types
            return NotImplemented
        return self.presence == other.presence and self.last_updated == other.last_updated


class MotionSensor(Sensor):

    def __init__(self, id, unique_id, name, sensor_type, presence: bool, last_update: str):
        super().__init__(id, name, sensor_type)
        self.unique_id = unique_id
        self.state = MotionSensorState(presence, last_update)
        self.last_states = []

    def add_state(self, state: MotionSensorState):
        self.last_states.append(state)
        self.state = state

    def state_changed(self):
        try:
            return self.last_states[-1] != self.last_states[-2]
        except IndexError:
            return False
