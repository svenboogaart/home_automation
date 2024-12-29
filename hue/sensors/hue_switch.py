from dataclasses import dataclass
from typing import List

from helpers.enums.hue_dimmer_event import HueDimmerEvent
from helpers.enums.sensor_types import SensorType
from hue.sensors.sensor_abc import SensorABC
from interfaces.sensors.i_switch import ISwitch


@dataclass
class SwitchState:
    button_event: HueDimmerEvent
    last_updated: float


class HueSwitch(SensorABC, ISwitch):

    def __init__(self, sensor_id: id, unique_id: str, name: str, sensor_type: SensorType, button_event: HueDimmerEvent,
                 last_updated: float):
        super().__init__(sensor_id, name, sensor_type)
        self.unique_id = unique_id
        self.switch_state = SwitchState(button_event, last_updated)
        self.last_states: List[SwitchState] = [self.switch_state]

    def add_state(self, state: SwitchState):
        if len(self.last_states) > 500:
            del self.last_states[0]
        self.last_states.append(state)
        self.switch_state = state

    def state_changed(self):
        try:
            return self.last_states[-1] != self.last_states[-2]
        except IndexError:
            return False

    def is_release_long_click(self):
        if len(self.last_states) >= 2:
            return (self.last_states[-1].button_event.is_released_event() and
                    self.last_states[-2].button_event.is_hold_event())
        return False

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
