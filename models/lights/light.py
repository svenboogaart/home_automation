from helpers.enums.device_state import DeviceState
from models.lights.LightState import LightState


class Light:

    def __init__(self, id, unique_id, name, min_dim_level, max_lumen, light_type, brightness, hue, saturation,
                 device_state: DeviceState = DeviceState.UNKNOWN, ):
        self.id = id
        self.unique_id = unique_id
        self.name = name
        self.min_dim_level = min_dim_level
        self.max_lumen = max_lumen
        self.light_type = light_type
        self.light_state = LightState(brightness, hue, saturation, device_state)
        self.last_states = [self.light_state]

    def add_state(self, state: LightState):
        self.light_state = state
        self.last_states.append(state)

    def state_changed(self):
        if len(self.last_states) < 2:
            return True
        try:
            return self.last_states[-1] != self.last_states[-2]
        except IndexError:
            return False
