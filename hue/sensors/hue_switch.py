from typing import List

from helpers.enums.hue_dimmer_event import HueDimmerEvent
from hue.sensors.sensor import Sensor
from interfaces.sensors.i_switch import ISwitch


class SwitchState:

    def __init__(self, button_event: HueDimmerEvent, last_updated):
        self.button_event = button_event
        self.last_updated = last_updated

    def __eq__(self, other):
        if not isinstance(other, SwitchState):
            # don't attempt to compare against unrelated types
            return NotImplemented

        return self.button_event == other.button_event and self.last_updated == other.last_updated


class HueSwitch(Sensor, ISwitch):

    def __init__(self, sensor_id, unique_id, name, sensor_type, button_event, last_updated):
        super().__init__(sensor_id, name, sensor_type)
        self.unique_id = unique_id
        self.switch_state = SwitchState(button_event, last_updated)
        self.last_states: List[SwitchState] = [self.switch_state]

    def add_state(self, state: SwitchState):
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

    def get_last_update_date(self):
        try:
            return self.last_states[-1].last_updated
        except IndexError:
            return False

    def get_name(self):
        return self.name

    def button_off_used(self) -> bool:
        try:
            return self.last_states[-1].button_event.is_hold_event()
        except IndexError:
            return False
