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


class Settings:

    def __init__(self):
        load_dotenv()
        self.hue_username = os.getenv(ENV_HUE_USER_KEY)
        self.hue_ip_address = os.getenv(ENV_HUE_IP_ADDRESS_KEY)
        self.twilio_auth_token = os.getenv(TWILIO_AUTH_TOKEN)
        self.twilio_account_ssd = os.getenv(TWILIO_ACCOUNT_SID)
        self.twilio_phone_number = os.getenv(TWILIO_PHONE_NUMBER)
        self.sms_receiver_number = os.getenv(SMS_RECEIVER_NUMBER)
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
