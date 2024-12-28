from dataclasses import dataclass

from helpers.enums.device_state import DeviceState


@dataclass
class LightState:
    brightness: int
    hue: int
    saturation: int
    device_state: DeviceState
