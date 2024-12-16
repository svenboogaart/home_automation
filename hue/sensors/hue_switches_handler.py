from typing import List

from hue.sensors.hue_sensors_manager import HueSensorsManager
from hue.sensors.hue_switch import HueSwitch
from interfaces.handlers.i_switches_handler import ISwitchesHandler


class HueSwitchesHandler(ISwitchesHandler):

    def __init__(self, hue_sensor_manager: HueSensorsManager):
        self.known_switches: dict[str, HueSwitch] = {}
        self._hue_sensor_manager = hue_sensor_manager

    def update_switches(self):
        for switch in self._hue_sensor_manager.get_switches():
            self.update_switch(switch)

    def get_switches(self) -> List[HueSwitch]:
        return list(self.known_switches.values())

    def update_switch(self, switch: HueSwitch):

        if switch.get_unique_id() in self.known_switches:
            self.known_switches[switch.get_unique_id()].add_state(switch.switch_state)
        else:
            self.known_switches[switch.get_unique_id()] = switch


