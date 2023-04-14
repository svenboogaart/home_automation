import time

from database.DataLayer import DataLayer
from database.migration import Migration
from hue.hue_connector import HueConnector
from hue.lights.lights_manager import LightsManager

TICK_TIME_SECONDS = 5


class Brain:

    def __init__(self):
        self.hue_connection = HueConnector()
        self.database_layer = DataLayer()
        self.lights_manager = LightsManager(self.hue_connection, self.database_layer)

    def control_automation(self):
        self.start_brain()
        print("The home is now running in automation mode.")
        starttime = time.time()
        while True:
            time.sleep(5.0 - ((time.time() - starttime) % 5.0))
            self.update()

    def start_brain(self):
        print("preparing brain")
        migration = Migration(self.lights_manager)
        migration.migrate()
        self.database_layer.store_lights(self.lights_manager.get_lights())

    def update(self):
        self.database_layer.log_light_states(self.lights_manager.get_lights())
        print("doing things")
