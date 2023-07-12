import os
from dotenv import load_dotenv

ENV_HUE_USER_KEY = "HUE_USER"
ENV_HUE_IP_ADDRESS_KEY = "HUE_IP_ADDRESS"
LOG_DATA = "LOG_DATA"
ALARM_MP3_PATH = "ALARM_MP3_PATH"
ALARM_PLAY_SOUND = "ALARM_PLAY_SOUND"


class Settings:

    def __init__(self):
        load_dotenv()
        self.hue_username = os.getenv(ENV_HUE_USER_KEY)
        self.hue_ip_address = os.getenv(ENV_HUE_IP_ADDRESS_KEY)
        self.alarm_mp3_file = os.getenv(ALARM_MP3_PATH)
        self.alarm_play_sound = os.getenv(ALARM_PLAY_SOUND) == "TRUE"
        self.should_log_data = os.getenv(LOG_DATA) == "True"

        self.alarm_active = False

    def set_alarm_active_state(self, state_to_set_alarm):
        if not state_to_set_alarm and self.alarm_active:
            self.alarm_active = False
            print("Turning alarm off")
        elif state_to_set_alarm and not self.alarm_active:
            self.alarm_active = True
            print("Turning alarm on")
