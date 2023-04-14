from enums.device_state import DeviceState
from hue.lights.LightState import LightState


class Light:

    def __init__(self, id, unique_id, name, min_dim_level, max_lumen, light_type, brightness, hue, saturation, device_state: DeviceState = DeviceState.UNKNOWN, ):
        self.id = id
        self.unique_id = unique_id
        self.name = name
        self.min_dim_level = min_dim_level
        self.max_lumen = max_lumen
        self.light_type = light_type
        self.light_state = LightState(brightness, hue, saturation, device_state)

