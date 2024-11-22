"""Module providing a base class for a hue manager."""
from abc import ABC

from hue.hue_connector import HueConnector


class HueManagerAbc(ABC):

    def __init__(self, hue_connector: HueConnector):
        self.hue_connector = hue_connector
