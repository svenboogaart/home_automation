from typing import List

from hue.data_loader.hue_sensors_loader import HueSensorsLoader
from hue.sensors.hue_switch import HueSwitch
from interfaces.handlers.i_switches_handler import ISwitchesHandler


class HueSwitchesHandler(ISwitchesHandler):

    def __init__(self, hue_sensor_loader: HueSensorsLoader):
        self.known_switches: dict[str, HueSwitch] = {}
        self._hue_sensor_loader = hue_sensor_loader

    def update_switches(self):
        for switch in self._hue_sensor_loader.get_switches():
            self.update_switch(switch)

    def get_switches(self) -> List[HueSwitch]:
        return list(self.known_switches.values())

    def update_switch(self, switch: HueSwitch):

        if switch.get_unique_id() in self.known_switches:
            self.known_switches[switch.get_unique_id()].add_state(switch.get_state())
        else:
            self.known_switches[switch.get_unique_id()] = switch
