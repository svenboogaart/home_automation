import unittest

from helpers.enums.sensor_types import SensorType
from hue.sensors.hue_switch import HueSwitch, SwitchState


class HueSwitchTests(unittest.TestCase):
    def test_unrecognized_button_event_is_treated_as_no_event(self):
        switch = HueSwitch(
            1,
            "switch-1",
            "Test switch",
            SensorType.SWITCH,
            SwitchState(None, 0),
        )

        self.assertFalse(switch.is_pressed_event())
        self.assertFalse(switch.is_released_event())
        self.assertFalse(switch.is_hold_event())
        self.assertFalse(switch.button_off_used())
        self.assertFalse(switch.button_on_used())
        self.assertIsNone(switch.get_last_event_code())


if __name__ == "__main__":
    unittest.main()
