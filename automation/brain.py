import time

from hue.hue_connector import HueConnector

TICK_TIME_SECONDS = 5

class Brain:

    def control_automation(self):
        print("The home is now running in atuomation mode.")
        self.hue_connection = HueConnector()
        self.hue_connection.connect()

        starttime = time.time()
        while True:
            print("tick")
            time.sleep(5.0 - ((time.time() - starttime) % 5.0))
            self.update()

    def update(self):
        print("doing things")