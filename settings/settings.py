import os
from dotenv import load_dotenv

ENV_HUE_USER_KEY = "HUE_USER"
ENV_HUE_IP_ADDRESS_KEY = "HUE_IP_ADDRESS"

class Settings:

    def __init__(self):
        load_dotenv()
        self.hue_username = os.getenv(ENV_HUE_USER_KEY)
        self.hue_ip_address = os.getenv(ENV_HUE_IP_ADDRESS_KEY)
