from enums.device_state import DeviceState


class Light:

    def __init__(self, id, name, min_dim_level, max_lumen, light_type, state: DeviceState = DeviceState.UNKNOWN):
        self.id = id
        self.name = name
        self.min_dim_level = min_dim_level
        self.max_lumen = max_lumen
        self.light_type = light_type
        self.state: DeviceState = state

