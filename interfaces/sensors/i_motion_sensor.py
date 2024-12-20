from abc import ABCMeta, abstractmethod


class MotionSensorState:

    def __init__(self, presence: bool, last_updated):
        self.presence = presence
        self.last_updated = last_updated

    def __eq__(self, other):
        if not isinstance(other, MotionSensorState):
            # don't attempt to compare against unrelated types
            return NotImplemented
        return self.presence == other.presence and self.last_updated == other.last_updated


class IMotionSensor(metaclass=ABCMeta):
    @abstractmethod
    def state_changed(self):
        pass

    @abstractmethod
    def motion_detected(self):
        pass

    @abstractmethod
    def get_unique_id(self):
        pass

    @abstractmethod
    def get_last_update_date(self):
        pass

    @abstractmethod
    def get_name(self):
        pass

    @abstractmethod
    def add_state(self, state: MotionSensorState):
        pass

    @abstractmethod
    def get_state(self) -> MotionSensorState:
        pass

    @abstractmethod
    def new_motion_detected(self):
        pass
