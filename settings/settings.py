import os
from dotenv import load_dotenv

ENV_HUE_USER_KEY = "HUE_USER"
ENV_HUE_IP_ADDRESS_KEY = "HUE_IP_ADDRESS"
LOG_DATA = "LOG_DATA"


class Settings:

    def __init__(self):
        load_dotenv()
        self.hue_username = os.getenv(ENV_HUE_USER_KEY)
        self.hue_ip_address = os.getenv(ENV_HUE_IP_ADDRESS_KEY)
        self.should_log_data = os.getenv(LOG_DATA) == "True"
        self.alarm_active = False
