import os

from dotenv import load_dotenv

# pylint: disable=R0903

ENV_HUE_USER_KEY = "HUE_USER"
ENV_HUE_IP_ADDRESS_KEY = "HUE_IP_ADDRESS"
LOG_DATA = "LOG_DATA"
MP3_PATH_ALARM = "MP3_PATH_ALARM"
MP3_PATH_ACTIVATED = "MP3_PATH_ACTIVATED"
MP3_PATH_DEACTIVATED = "MP3_PATH_DEACTIVATED"
ALARM_PLAY_SOUND = "ALARM_PLAY_SOUND"
TWILIO_AUTH_TOKEN = "TWILIO_AUTH_TOKEN"
TWILIO_ACCOUNT_SID = "TWILIO_ACCOUNT_SID"
TWILIO_PHONE_NUMBER = "TWILIO_PHONE_NUMBER"
SMS_RECEIVER_NUMBER = "SMS_RECEIVER_NUMBER"
HUE_STATUS_LIGHT_ID = "HUE_STATUS_LIGHT_ID"
SEND_MAIL = "SEND_MAIL"
LOCATION = "LOCATION"
MAIL_TO = "MAIL_TO"
MAIL_FROM = "MAIL_FROM"
MAIL_PASSWORD = "MAIL_PASSWORD"


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
        self.alarm_play_sound = os.getenv(ALARM_PLAY_SOUND, None) == "True"
        self.mp3_file_alarm = os.getenv(MP3_PATH_ALARM, None)
        self.mp3_path_activated = os.getenv(MP3_PATH_ACTIVATED, None)
        self.mp3_path_deactivated = os.getenv(MP3_PATH_DEACTIVATED, None)
        self.should_log_data = os.getenv(LOG_DATA, None) == "True"
        self.send_mail = os.getenv(SEND_MAIL, None) == "True"
        self.mail_from = os.getenv(MAIL_FROM, None)
        self.mail_password = os.getenv(MAIL_PASSWORD, None)
        self.location = os.getenv(LOCATION, None)
        self.mail_to = os.getenv(MAIL_TO, None)
