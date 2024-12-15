from helpers.enums.device_state import DeviceState
from models.lights.LightState import LightState
from interfaces.lights.i_light import ILight


class HueLight(ILight):

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
            last_state =  self.last_states[-1]
            previous_state = self.get_previous_light_state()
            return last_state.device_state != previous_state.device_state
        except IndexError:
            return False

    def get_unique_id(self) -> str:
        return self.unique_id

    def get_name(self) -> str:
        return self.name

    def get_type(self) -> str:
        return self.light_type

    def get_light_state(self) ->LightState:
        try:
            return self.last_states[-1]
        except IndexError:
            return None

    def get_previous_light_state(self) -> LightState:
        try:
            return self.last_states[-2]
        except IndexError:
            return None

