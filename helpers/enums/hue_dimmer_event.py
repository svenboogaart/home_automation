from enum import Enum


class HueDimmerEvent(Enum):
    HARD_PRESS_ON = 1000
    LONG_PRESS_ON = 1001
    RELEASE_ON = 1003
    SOFT_PRESS_ON = 1002
    HARD_PRESS_BRIGHTER = 2000
    LONG_PRESS_BRIGHTER = 2001
    RELEASE_BRIGHTER = 2003
    SOFT_PRESS_BRIGHTER = 2002
    HARD_PRESS_DARKER = 3000
    LONG_PRESS_DARKER = 3001
    RELEASE_DARKER = 3003
    SOFT_PRESS_DARKER = 3002
    HARD_PRESS_OFF = 4000
    LONG_PRESS_OFF = 4001
    RELEASE_OFF = 4003
    SOFT_PRESS_OFF = 4002

    def is_released_event(self) -> bool:
        """Check if the event represents a 'released' state."""
        released_events = {
            HueDimmerEvent.RELEASE_ON,
            HueDimmerEvent.RELEASE_BRIGHTER,
            HueDimmerEvent.RELEASE_DARKER,
            HueDimmerEvent.RELEASE_OFF,
        }
        return self in released_events

    def is_pressed_event(self) -> bool:
        """Check if the event represents a 'pressed' state (i.e., any kind of press)."""
        pressed_events = {
            HueDimmerEvent.HARD_PRESS_ON,
            HueDimmerEvent.SOFT_PRESS_ON,
            HueDimmerEvent.HARD_PRESS_BRIGHTER,
            HueDimmerEvent.SOFT_PRESS_BRIGHTER,
            HueDimmerEvent.HARD_PRESS_DARKER,
            HueDimmerEvent.SOFT_PRESS_DARKER,
            HueDimmerEvent.HARD_PRESS_OFF,
            HueDimmerEvent.SOFT_PRESS_OFF
        }
        return self in pressed_events

    def is_hold_event(self) -> bool:
        """Check if the event represents a 'hold' (long press) state."""
        hold_events = {
            HueDimmerEvent.LONG_PRESS_ON,
            HueDimmerEvent.LONG_PRESS_BRIGHTER,
            HueDimmerEvent.LONG_PRESS_DARKER,
            HueDimmerEvent.LONG_PRESS_OFF,
        }
        return self in hold_events
