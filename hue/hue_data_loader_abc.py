"""Module providing a base class for a hue manager."""
from abc import ABC

from interfaces.i_hue_connector import IHueConnector


# pylint: disable=R0903

class HueDataLoaderAbc(ABC):
    """
    Abstract base class for loading data for Hue devices.

    Subclasses must take a hue_connector to be able to get the hue info.
    """

    def __init__(self, hue_connector: IHueConnector):
        self.hue_connector = hue_connector
