import time

from helpers.enums.device_state import DeviceState
from hue.lights.lights_manager import LightsManager
from hue.sensors.switches_manager import SwitchesManager
from settings.settings import Settings
from twilio.rest import Client

TICK_TIME_SECONDS = 5
import os

class Brain:

    def __init__(self, database_layer, lights_manager : LightsManager, switches_manager: SwitchesManager, settings: Settings):
        self.database_layer = database_layer
        self.lights_manager = lights_manager
        self.switches_manager = switches_manager
        self.settings = settings
        self.sms_send_after_alarm_activated = False

    def control_automation(self):
        self.start_brain()
        print("The home is now running in automation mode.")
        starttime = time.time()
        while True:
            time.sleep(1.0 - ((time.time() - starttime) % 1.0))
            self.update()

    def start_brain(self):
        print("Preparing brain")
        self.database_layer.store_lights(self.lights_manager.get_lights())
        self.database_layer.store_switches(self.switches_manager.get_switches())

    def update(self):
        #print("Brain is processing data.")
        self.__update_device_states()
        self.__log_data()
        self.__event_based_processing()

    def __update_device_states(self):
        self.lights_manager.update_lights()
        self.switches_manager.update_switches()

    def __log_data(self):
        if self.settings.should_log_data:
            self.database_layer.log_light_states(self.lights_manager.get_lights())

    def __event_based_processing(self):
        self.__process_switch_events()
        self.__process_light_events()

    def __process_light_events(self):
        for light in self.lights_manager.get_lights():
            if light.state_changed():
                #print(light.unique_id, " Light changed to ", light.light_state.device_state, " was ", light.last_states[-2].device_state)
                if self.settings.alarm_active and light.light_state.device_state == DeviceState.ON:
                    print("Intruder detected")
                    if self.settings.alarm_play_sound:
                        os.system('say "Intruder detected, calling police."')
                        os.system(f"afplay {self.settings.alarm_mp3_file}")
                    self.__send_sms("Intruder alarm")

    def __process_switch_events(self):
        for switch in self.switches_manager.get_switches():
            if switch.state_changed():
                if switch.switch_state.release_hold and switch.switch_state.button_pressed == 4:
                    self.settings.set_alarm_active_state(True)
                elif switch.switch_state.release_hold and switch.switch_state.button_pressed == 1 :
                    self.settings.set_alarm_active_state(False)
                    self.sms_send_after_alarm_activated = False

    def __send_sms(self, content):
        if not self.sms_send_after_alarm_activated and self.settings.twilio_account_ssd:
            client = Client(self.settings.twilio_account_ssd, self.settings.twilio_auth_token)

            message = client.messages.create(
                from_= "svenhome",
                body = content,
                to = self.settings.sms_receiver_number
            )
            self.sms_send_after_alarm_activated = True
            print(f"Sms has been send: {message.sid}")
        else:
            print("No sms has been send")



