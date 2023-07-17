import time
from threading import Thread

from helpers.enums.hue_colors import HueColor
from models.managers.audio_manager import AudioManager
from models.managers.lights_manager import LightsManager
from models.managers.motion_sensor_manager import MotionSensorManager
from models.managers.sms_manager import SmsManager
from models.managers.switches_manager import SwitchesManager
from settings.settings import Settings
from twilio.rest import Client

TICK_TIME_SECONDS = 5
import os


class Brain:

    def __init__(self, database_layer, lights_manager: LightsManager, switches_manager: SwitchesManager,
                 motion_sensor_manager: MotionSensorManager, audio_manager: AudioManager, sms_manager: SmsManager,
                 settings: Settings):
        self.database_layer = database_layer
        self.lights_manager = lights_manager
        self.switches_manager = switches_manager
        self.motion_sensor_manager = motion_sensor_manager
        self.audio_manager = audio_manager
        self.sms_manager = sms_manager
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
        # print("Brain is processing data.")
        self.__update_device_states()
        self.__log_data()
        self.__event_based_processing()

    def __update_device_states(self):
        self.lights_manager.update_lights()
        self.switches_manager.update_switches()
        self.motion_sensor_manager.update_sensors()

    def __log_data(self):
        if self.settings.should_log_data:
            self.database_layer.log_light_states(self.lights_manager.get_lights())

    def __event_based_processing(self):
        self.__process_switch_events()
        self.__process_motion_events()
        self.__process_light_events()

    def __process_light_events(self):
        if self.settings.alarm_active:
            for light in self.lights_manager.get_lights():
                if light.state_changed():
                    pass
                    # #print(light.unique_id, " Light changed to ", light.light_state.device_state, " was ", light.last_states[-2].device_state)
                    # if light.light_state.device_state == DeviceState.ON:
                    #     print("Intruder detected")
                    #     if self.settings.alarm_play_sound:
                    #         os.system('say "Intruder detected, calling police."')
                    #         os.system(f"afplay {self.settings.alarm_mp3_file}")
                    #     if not self.sms_send_after_alarm_activated and self.settings.twilio_account_ssd:
                    #         self.__send_sms("Intruder alarm")
                    #     if self.settings.hue_status_light:
                    #         self.lights_manager.alarm_light(self.settings.hue_status_light, 0.2, 0.2, 3)

    def __process_switch_events(self):
        for switch in self.switches_manager.get_switches():
            if switch.state_changed():
                if switch.state.release_hold and switch.state.button_pressed == 4:
                    if self.settings.set_alarm_active_state(True):
                        self.lights_manager.alarm_light(self.settings.hue_status_light, 0.5, 0.5, 2)
                        self.audio_manager.play_activated_sound()
                elif switch.state.release_hold and switch.state.button_pressed == 1:
                    if self.settings.set_alarm_active_state(False):
                        self.lights_manager.alarm_light(self.settings.hue_status_light, 0.5, 0.5, 2, HueColor.GREEN)
                        self.audio_manager.play_deactivate_sound()

    def __send_sms(self, content):
        client = Client(self.settings.twilio_account_ssd, self.settings.twilio_auth_token)

        message = client.messages.create(
            from_="svenhome",
            body=content,
            to=self.settings.sms_receiver_number
        )
        self.sms_send_after_alarm_activated = True
        print(f"Sms has been send: {message.sid}")

    def __process_motion_events(self):
        if self.settings.alarm_active:
            for motion_sensor in self.motion_sensor_manager.get_sensors():
                if motion_sensor.state_changed() and motion_sensor.state.presence:
                    print("Motion detected!")
                    if self.settings.alarm_play_sound:
                        self.audio_manager.play_alarm_sound()
                    if not self.sms_send_after_alarm_activated:
                        self.sms_manager.send_sms("Intruder alarm")
                    if self.settings.hue_status_light:
                        self.lights_manager.alarm_light(self.settings.hue_status_light, 1.0, 2.0, 2)
