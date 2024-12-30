"""Contains all the processing logic for home automation."""

import time
from datetime import datetime

from helpers.enums.hue_colors import HueColor
from interfaces.handlers.i_daylight_sensor_handler import IDaylightSensorHandler
from interfaces.handlers.i_temperature_sensor_handler import ITemperatureSensorHandler
from models.managers.audio_manager import AudioManager
from models.managers.lights_manager import LightsManager
from models.managers.mail_manager import MailManager
from models.managers.motion_sensor_manager import MotionSensorManager
from models.managers.sms_manager import SmsManager
from models.managers.switches_manager import SwitchesManager
from settings.settings import Settings

TICK_TIME_SECONDS = 2


class Brain:

    def __init__(self, database_layer, lights_manager: LightsManager, switches_manager: SwitchesManager,
                 motion_sensor_manager: MotionSensorManager, temperature_sensor_handler: ITemperatureSensorHandler,
                 daylight_sensor_handler: IDaylightSensorHandler,
                 audio_manager: AudioManager, sms_manager: SmsManager,
                 mail_manager: MailManager, settings: Settings):
        self.__database_layer = database_layer
        self.__lights_manager = lights_manager
        self.__switches_manager = switches_manager
        self.__motion_sensor_manager = motion_sensor_manager
        self.__daylight_sensor_handler = daylight_sensor_handler
        self.__temperature_sensor_handler = temperature_sensor_handler
        self.__audio_manager = audio_manager
        self.__mail_manager = mail_manager
        self.__sms_manager = sms_manager
        self.__settings = settings
        self.__sms_send_after_alarm_activated = False
        self.__alarm_active = False
        self.__alarm_activated_timestamp = 0

    def control_automation(self):
        self.start_brain()
        print("The home is now running in automation mode.")
        start_time = time.time()
        while True:
            time.sleep(1.0 - ((time.time() - start_time) % 1.0))
            self.update()

    def start_brain(self):
        print(f"Preparing brain, Alarm state: {self.__alarm_active}")
        # self.database_layer.store_lights(self.lights_manager.get_lights())
        # self.database_layer.store_switches(self.switches_manager.get_switches())

    def update(self):
        # print("Brain is processing data.")
        self.__update_device_states()
        self.__log_data()
        self.__event_based_processing()

    def __update_device_states(self):
        self.__lights_manager.update_lights()
        self.__switches_manager.update_switches()
        self.__motion_sensor_manager.update_motion_sensors()
        self.__daylight_sensor_handler.update_daylight_sensors()
        self.__temperature_sensor_handler.update_temperature_sensors()

    def __log_data(self):
        try:
            if self.__settings.should_log_data:
                # Register all devices
                self.__database_layer.store_lights(self.__lights_manager.get_lights())
                self.__database_layer.store_switches(self.__switches_manager.get_switches())
                self.__database_layer.log_motion_sensors(self.__motion_sensor_manager.get_motion_sensors())
                self.__database_layer.log_daylight_sensors(self.__daylight_sensor_handler.get_daylight_sensors())
                self.__database_layer.log_temperature_sensors(
                    self.__temperature_sensor_handler.get_temperature_sensors())

                for switch in self.__switches_manager.get_switches():
                    if switch.state_changed():
                        self.__database_layer.log_switch_event(switch)

                for light in self.__lights_manager.get_lights():
                    if light.state_changed():
                        self.__database_layer.log_light_state(light)

                for motion_sensor in self.__motion_sensor_manager.get_motion_sensors():
                    if motion_sensor.state_changed():
                        self.__database_layer.log_motion_sensor_event(motion_sensor)

                for daylight_sensor in self.__daylight_sensor_handler.get_daylight_sensors():
                    if daylight_sensor.state_changed():
                        self.__database_layer.log_daylight_sensor_event(daylight_sensor)

                for temperature_sensor in self.__temperature_sensor_handler.get_temperature_sensors():
                    if temperature_sensor.state_changed():
                        self.__database_layer.log_temperature_sensor_event(temperature_sensor)
        except Exception as e:
            print(f"Failed to save the data in the database {e}")

    def __event_based_processing(self):
        self.__process_switch_events()
        self.__process_motion_events()
        self.__process_light_events()

    def __process_light_events(self):
        if self.__alarm_active:
            for light in self.__lights_manager.get_lights():
                if light.state_changed():
                    pass
                    # try:
                    #     # print(light.get_unique_id(), " Light changed to ", light.get_light_state().device_state,
                    #     #       "from ", light.get_previous_light_state().device_state)
                    # except:
                    #     print("Something went wrong")
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
        for switch in self.__switches_manager.get_switches():
            if switch.state_changed():
                if switch.is_release_long_click() and switch.button_off_used():
                    if self.__alarm_active:
                        self.__lights_manager.alarm_light(self.__settings.hue_status_light, 0.5, 0.5, 2, HueColor.GREEN)
                        self.__audio_manager.play_deactivate_sound()
                        print("Alarm deactivated")
                        self.__alarm_active = False
                        self.__alarm_activated_timestamp = 0
                elif switch.is_release_long_click() and switch.button_on_used():
                    if not self.__alarm_active:
                        self.__lights_manager.alarm_light(self.__settings.hue_status_light, 0.5, 0.5, 4)
                        self.__audio_manager.play_activated_sound()
                        print("Alarm activated")
                        self.__alarm_active = True
                        self.__alarm_activated_timestamp = int(datetime.timestamp(datetime.now()))

    def __get_seconds_after_alarm_activate(self) -> int:
        return int(datetime.timestamp(datetime.now())) - self.__alarm_activated_timestamp

    def __process_motion_events(self):
        for motion_sensor in self.__motion_sensor_manager.get_motion_sensors():
            if motion_sensor.new_motion_detected():
                if self.__alarm_active:
                    if self.__get_seconds_after_alarm_activate() > 10:
                        print("Motion detected!")
                        if self.__settings.alarm_play_sound:
                            self.__audio_manager.play_alarm_sound()
                            self.__audio_manager.say_something("Intruder detected, calling the police")
                        if self.__settings.send_mail:
                            self.__mail_manager.send_mail("Intruder detected", self.__settings.mail_to)
                        if not self.__sms_send_after_alarm_activated:
                            self.__sms_manager.send_sms("Intruder alarm")
                        if self.__settings.hue_status_light:
                            self.__lights_manager.alarm_light(self.__settings.hue_status_light, 1.0, 2.0, 2)
                    else:
                        print("Alarm is activating, ignoring the first seconds")
                else:
                    print("Motion detected, but alarm is not active.")
