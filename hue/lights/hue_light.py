from interfaces.lights.i_light import ILight
from models.lights.light_state import LightState


class HueLight(ILight):

    def __init__(self, light_id, unique_id, name, min_dim_level, max_lumen, light_type, light_state: LightState,
                 last_updated: float):
        self.id = light_id
        self.unique_id = unique_id
        self.name = name
        self.min_dim_level = min_dim_level
        self.max_lumen = max_lumen
        self.light_type = light_type
        self.light_state = light_state
        self.last_states = [self.light_state]
        self.last_updated = last_updated

    def add_state(self, state: LightState):
        if len(self.last_states) > 500:
            del self.last_states[0]
        self.light_state = state
        self.last_states.append(state)

    def state_changed(self):
        if len(self.last_states) < 2:
            return True
        try:
            last_state = self.last_states[-1]
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

    def get_light_state(self) -> LightState | None:
        try:
            return self.last_states[-1]
        except IndexError:
            return None

    def get_previous_light_state(self) -> LightState | None:
        try:
            return self.last_states[-2]
        except IndexError:
            return None

    def get_last_update_date(self) -> float:
        return self.last_updated
