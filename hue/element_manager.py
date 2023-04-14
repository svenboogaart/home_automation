from abc import ABC

from database.DataLayer import DataLayer
from hue.hue_connector import HueConnector


class ElementManager(ABC):

    def __init__(self, hue_connector: HueConnector):
        self.hue_connector = hue_connector
