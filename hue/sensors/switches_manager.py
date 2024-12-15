from typing import List

from hue.sensors.hue_sensors_manager import HueSensorsManager
from hue.sensors.hue_switch import HueSwitch


class SwitchesManager():
    known_switches = {}

    def __init__(self, sensor_manager: HueSensorsManager):
        self._motion_sensor_handler = sensor_manager

    def update_switches(self):
        for switch in self._motion_sensor_handler.get_switches():
            self.update_switch(switch)

    def get_switches(self) -> List[HueSwitch]:
        return list(self.known_switches.values())

    def update_switch(self, switch: HueSwitch):
        if switch.unique_id in self.known_switches:
            self.known_switches[switch.unique_id].add_state(switch.switch_state)
        else:
            self.known_switches[switch.unique_id] = switch

    def get_switch(self, id: int):
        if id in self.known_switches:
            return self.known_switches[id]
        return None
