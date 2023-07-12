from helpers.enums.device_state import DeviceState


class LightState:

    def __init__(self, brightness: int, hue: int, saturation: int, device_state):
        self.brightness = brightness
        self.hue = hue
        self.saturation = saturation
        self.device_state: DeviceState = device_state

    def __eq__(self, other):
        if not isinstance(other, LightState):
            # don't attempt to compare against unrelated types
            return NotImplemented

        return self.brightness == other.brightness and self.hue == other.hue and self.saturation == other.saturation and self.device_state == other.device_state
