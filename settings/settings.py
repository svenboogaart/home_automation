import os

from dotenv import load_dotenv

ENV_HUE_USER_KEY = "HUE_USER"
ENV_HUE_IP_ADDRESS_KEY = "HUE_IP_ADDRESS"
LOG_DATA = "LOG_DATA"
ALARM_MP3_PATH = "ALARM_MP3_PATH"
ALARM_PLAY_SOUND = "ALARM_PLAY_SOUND"
TWILIO_AUTH_TOKEN = "TWILIO_AUTH_TOKEN"
TWILIO_ACCOUNT_SID = "TWILIO_ACCOUNT_SID"
TWILIO_PHONE_NUMBER = "TWILIO_PHONE_NUMBER"
SMS_RECEIVER_NUMBER = "SMS_RECEIVER_NUMBER"
HUE_STATUS_LIGHT_ID = "HUE_STATUS_LIGHT_ID"


class Settings:

    def __init__(self):
        load_dotenv()
        self.hue_username = os.getenv(ENV_HUE_USER_KEY, None)
        self.hue_ip_address = os.getenv(ENV_HUE_IP_ADDRESS_KEY, None)
        self.twilio_auth_token = os.getenv(TWILIO_AUTH_TOKEN, None)
        self.twilio_account_ssd = os.getenv(TWILIO_ACCOUNT_SID, None)
        self.twilio_phone_number = os.getenv(TWILIO_PHONE_NUMBER, None)
        self.sms_receiver_number = os.getenv(SMS_RECEIVER_NUMBER, None)
        self.hue_status_light = os.getenv(HUE_STATUS_LIGHT_ID, None)
        self.alarm_mp3_file = os.getenv(ALARM_MP3_PATH, None)
        self.alarm_play_sound = os.getenv(ALARM_PLAY_SOUND, None) == "True"
        self.should_log_data = os.getenv(LOG_DATA, None) == "True"
        self.alarm_active = False

    def set_alarm_active_state(self, state_to_set_alarm) -> bool:
        if not state_to_set_alarm and self.alarm_active:
            self.alarm_active = False
            print("Turning alarm off")
            return True
        elif state_to_set_alarm and not self.alarm_active:
            self.alarm_active = True
            print("Turning alarm on")
            return True
        else:
            return False
