from typing import List

from interfaces.handlers.i_switches_handler import ISwitchesHandler
from interfaces.sensors.i_switch import ISwitch


class SwitchesManager:

    def __init__(self, switches_handler: ISwitchesHandler):
        self._switches_handler = switches_handler

    def update_switches(self):
        self._switches_handler.update_switches()

    def get_switches(self) -> List[ISwitch]:
        return self._switches_handler.get_switches()
