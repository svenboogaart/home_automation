"""Module providing a base class for a hue manager."""
from abc import ABC

from hue.hue_connector import HueConnector


# pylint: disable=R0903

class HueManagerAbc(ABC):
    """
    Abstract base class for managing Hue lights.

    Subclasses must take a hue_connector to be able to get the hue info.
    """
    def __init__(self, hue_connector: HueConnector):
        self.hue_connector = hue_connector
