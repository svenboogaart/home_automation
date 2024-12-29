from typing import List

from hue.sensors.hue_sensor_abc import HueSensorABC
from interfaces.sensors.i_daylight_sensor import IDaylightSensor, DayLightSensorState


class HueDayLightSensor(HueSensorABC, IDaylightSensor):

    def __init__(self, sensor_id, unique_id, name, sensor_type, sensor_state: DayLightSensorState):
        super().__init__(sensor_id, name, sensor_type)
        self.last_states: List[DayLightSensorState] = [sensor_state]
        self.unique_id = unique_id

    def get_last_update_date(self) -> float:
        return self.get_state().timestamp

    def get_unique_id(self) -> str:
        return self.unique_id

    def get_name(self) -> str:
        return self.name

    def get_state(self) -> DayLightSensorState:
        return self.last_states[-1]

    def daylight_detected(self) -> bool:
        return self.get_state().daylight_detected

    def add_state(self, state: DayLightSensorState):
        if len(self.last_states) > 500:
            del self.last_states[0]
        self.last_states.append(state)

    def state_changed(self):
        if len(self.last_states) < 2:
            return True
        return self.last_states[-1].daylight_detected != self.last_states[-2].daylight_detected

    def get_daylight_sensor_state(self) -> DayLightSensorState:
        return self.get_state()
