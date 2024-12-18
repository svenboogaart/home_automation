"""Contains all the processing logic for home automation."""

import time

from helpers.enums.hue_colors import HueColor
from models.managers.audio_manager import AudioManager
from models.managers.lights_manager import LightsManager
from models.managers.motion_sensor_manager import MotionSensorManager
from models.managers.sms_manager import SmsManager
from models.managers.switches_manager import SwitchesManager
from settings.settings import Settings

TICK_TIME_SECONDS = 5


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
        self.alarm_active = False

    def control_automation(self):
        self.start_brain()
        print("The home is now running in automation mode.")
        start_time = time.time()
        while True:
            time.sleep(1.0 - ((time.time() - start_time) % 1.0))
            self.update()

    def start_brain(self):
        print("Preparing brain")
        # self.database_layer.store_lights(self.lights_manager.get_lights())
        # self.database_layer.store_switches(self.switches_manager.get_switches())

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
            self.database_layer.store_lights(self.lights_manager.get_lights())
            self.database_layer.store_switches(self.switches_manager.get_switches())

            for switch in self.switches_manager.get_switches():
                if switch.state_changed():
                    self.database_layer.log_switch_event(switch)

            for light in self.lights_manager.get_lights():
                if light.state_changed():
                    self.database_layer.log_light_state(light)

            self.database_layer.log_motion_sensors(self.motion_sensor_manager.get_sensors())

            for motion_sensor in self.motion_sensor_manager.get_sensors():
                if motion_sensor.state_changed():
                    self.database_layer.log_motion_sensor_event(motion_sensor)

    def __event_based_processing(self):
        self.__process_switch_events()
        self.__process_motion_events()
        self.__process_light_events()

    def __process_light_events(self):
        if self.alarm_active:
            for light in self.lights_manager.get_lights():
                if light.state_changed():
                    try:
                        print(light.get_unique_id(), " Light changed to ", light.get_light_state().device_state,
                              "from ", light.get_previous_light_state().device_state)
                    except:
                        print("Something went wrong")
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
                if switch.is_release_long_click():
                    if not self.alarm_active:
                        self.lights_manager.alarm_light(self.settings.hue_status_light, 0.5, 0.5, 2)
                        self.audio_manager.play_activated_sound()
                        print("Alarm activated")
                        self.alarm_active = True
                    else:
                        self.lights_manager.alarm_light(self.settings.hue_status_light, 0.5, 0.5, 2, HueColor.GREEN)
                        self.audio_manager.play_deactivate_sound()
                        print("Alarm deactivated")
                        self.alarm_active = False

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

        for motion_sensor in self.motion_sensor_manager.get_sensors():
            if motion_sensor.motion_detected():
                if self.alarm_active:
                    print("Motion detected!")
                    if self.settings.alarm_play_sound:
                        self.audio_manager.play_alarm_sound()
                    if not self.sms_send_after_alarm_activated:
                        self.sms_manager.send_sms("Intruder alarm")
                    if self.settings.hue_status_light:
                        self.lights_manager.alarm_light(self.settings.hue_status_light, 1.0, 2.0, 2)
                else:
                    print("Motion detected, but alarm is not active.")
