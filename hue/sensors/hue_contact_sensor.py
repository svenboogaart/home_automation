from dataclasses import dataclass
from time import time
from typing import List

from helpers.enums.sensor_types import SensorType
from hue.sensors.hue_sensor_abc import HueSensorABC
from interfaces.sensors.i_contact_sensor import IContactSensor


@dataclass
class ContactState:
    has_contact: bool
    changed_timestamp: time
    data_loaded: time


class HueContactSensor(HueSensorABC, IContactSensor):

    def __init__(self, sensor_id: id, unique_id: str, name: str, state: ContactState):
        super().__init__(sensor_id, name, SensorType.CONTACT)
        self.unique_id = unique_id
        self.last_states: List[ContactState] = [state]

    def has_contact(self) -> bool:
        return self.get_state().has_contact

    def get_changed_timestamp(self) -> time:
        return self.get_state().changed_timestamp

    def get_state(self) -> ContactState:
        if len(self.last_states) > 0:
            return self.last_states[-1]

    def add_state(self, state: ContactState):
        if len(self.last_states) > 500:
            del self.last_states[0]
        self.last_states.append(state)

    def state_changed(self):
        if len(self.last_states) < 2:
            return True
        return self.last_states[-1].has_contact != self.last_states[-2].has_contact

    def get_unique_id(self):
        return self.unique_id

    def get_last_update_date(self) -> float:
        if len(self.last_states) == 0:
            return 0
        return self.last_states[-1].data_loaded

    def get_name(self):
        return self.name
