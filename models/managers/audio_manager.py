import os
from threading import Thread

from settings.settings import Settings


class AudioManager:

    def __init__(self, settings: Settings):
        self.__settings = settings

    def play_alarm_sound(self):
        if self.__settings.alarm_play_sound:
            Thread(target=os.system, args=('say "Intruder detected, calling police."',)).start()
            if self.__settings.alarm_mp3_file:
                self.__play_audio_file(self.__settings.alarm_mp3_file)

    def play_activated_sound(self):
        self.__play_audio_file('/Users/Sven/Documents/programming/python/home_automation/resources/audio/activated.wav')

    def play_deactivate_sound(self):
        self.__play_audio_file(
            '/Users/Sven/Documents/programming/python/home_automation/resources/audio/deactivated.wav')

    @staticmethod
    def __play_audio_file(filename: str):
        Thread(target=os.system, args=(f"afplay {filename}",)).start()
