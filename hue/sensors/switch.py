from hue.sensors.sensor import Sensor


class SwitchState:

    def __init__(self, button_event, last_updated):
        self.button_event = button_event
        self.last_updated = last_updated
        self.button_pressed = int(str(button_event)[0])

        last_digit = button_event % 10
        self.hold = last_digit == 1
        self.release = last_digit == 2
        self.release_hold = last_digit == 3

    def __eq__(self, other):
        if not isinstance(other, SwitchState):
            # don't attempt to compare against unrelated types
            return NotImplemented

        return self.button_event == other.button_event \
               and self.last_updated == other.last_updated \
               and self.button_pressed == other.button_pressed \
               and self.hold == other.hold \
               and self.release == other.release \
               and self.release_hold == other.release_hold


class Switch(Sensor):

    def __init__(self, id, unique_id, name, sensor_type, button_event, last_updated):
        super().__init__(id, name, sensor_type)
        self.unique_id = unique_id
        self.switch_state = SwitchState(button_event, last_updated)
        self.last_states = []

    def add_state(self, state: SwitchState):
        self.last_states.append(state)
        self.switch_state = state

    def state_changed(self):
        try:
            return self.last_states[-1] != self.last_states[-2]
        except IndexError:
            return False
