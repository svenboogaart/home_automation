from enums.device_state import DeviceState


class LightState:

    def __init__(self, brightness : int, hue : int, saturation : int, device_state):
        self.brightness = brightness
        self.hue = hue
        self.saturation = saturation
        self.device_state: DeviceState = device_state
