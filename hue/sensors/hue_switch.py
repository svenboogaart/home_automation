from dataclasses import dataclass
from typing import List

from helpers.enums.hue_dimmer_event import HueDimmerEvent
from helpers.enums.sensor_types import SensorType
from hue.sensors.hue_sensor_abc import HueSensorABC
from interfaces.sensors.i_switch import ISwitch


@dataclass
class SwitchState:
    button_event: HueDimmerEvent
    last_updated: float


class HueSwitch(HueSensorABC, ISwitch):

    def __init__(self, sensor_id: id, unique_id: str, name: str, sensor_type: SensorType, switch_sate: SwitchState):
        super().__init__(sensor_id, name, sensor_type)
        self.unique_id = unique_id
        self.last_states: List[SwitchState] = [switch_sate]

    def get_state(self) -> SwitchState:
        if len(self.last_states) > 0:
            return self.last_states[-1]

    def add_state(self, state: SwitchState):
        if len(self.last_states) > 500:
            del self.last_states[0]
        self.last_states.append(state)

    def state_changed(self):
        if len(self.last_states) < 2:
            return True
        return self.last_states[-1] != self.last_states[-2]

    def is_release_long_click(self):
        if len(self.last_states) >= 2:
            return (self.last_states[-1].button_event.is_released_event() and
                    self.last_states[-2].button_event.is_hold_event())
        return False

    def get_last_event_code(self) -> int:
        return self.get_state().button_event

    def is_pressed_event(self):
        try:
            return self.last_states[-1].button_event.is_pressed_event()
        except IndexError:
            return False

    def is_released_event(self):
        try:
            return self.last_states[-1].button_event.is_released_event()
        except IndexError:
            return False

    def is_hold_event(self):
        try:
            return self.last_states[-1].button_event.is_hold_event()
        except IndexError:
            return False

    def get_unique_id(self):
        return self.unique_id

    def get_last_update_date(self) -> float:
        if len(self.last_states) == 0:
            return 0
        return self.last_states[-1].last_updated

    def get_name(self):
        return self.name

    def button_off_used(self) -> bool:
        try:
            return self.last_states[-1].button_event.is_off_event()
        except IndexError:
            return False

    def button_on_used(self) -> bool:
        try:
            return self.last_states[-1].button_event.is_on_event()
        except IndexError:
            return False
