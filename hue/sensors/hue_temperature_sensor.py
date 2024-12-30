from typing import List

from hue.sensors.hue_sensor_abc import HueSensorABC
from interfaces.sensors.i_temperature_sensor import ITemperatureSensor, TemperatureSensorState


class HueTemperatureSensor(HueSensorABC, ITemperatureSensor):

    def __init__(self, sensor_id, unique_id, name, sensor_type, sensor_state: TemperatureSensorState):
        super().__init__(sensor_id, name, sensor_type)
        self.last_states: List[TemperatureSensorState] = [sensor_state]
        self.unique_id = unique_id

    def get_last_update_date(self) -> float:
        return self.get_state().timestamp

    def get_unique_id(self) -> str:
        return self.unique_id

    def get_name(self) -> str:
        return self.name

    def get_state(self) -> TemperatureSensorState:
        return self.last_states[-1]

    def get_temperature(self) -> float:
        return self.get_state().temperature

    def add_state(self, state: TemperatureSensorState):
        if len(self.last_states) > 500:
            del self.last_states[0]
        self.last_states.append(state)

    def state_changed(self):
        if len(self.last_states) < 2:
            return True
        return self.last_states[-1].timestamp != self.last_states[-2].timestamp or self.last_states[-1].temperature != \
            self.last_states[-2].temperature
