import os
from threading import Thread
from playsound import playsound
from settings.settings import Settings


class AudioManager:

    def __init__(self, settings: Settings):
        self.__settings = settings

    def play_alarm_sound(self):
        if self.__settings.alarm_play_sound:
            Thread(target=os.system, args=('say "Intruder detected, calling police."',)).start()
            self.__play_audio_file(self.__settings.mp3_file_alarm)

    def play_activated_sound(self):
        self.__play_audio_file(self.__settings.mp3_path_activated)

    def play_deactivate_sound(self):
        self.__play_audio_file(self.__settings.mp3_path_deactivated)

    @staticmethod
    def __play_audio_file(file_path: str):
        try:
            if os.path.isfile(file_path):
                playsound(file_path)
            else:
                print("Failed to play audo, %s file not found " % file_path)
        except Exception as e:
            print("Failed to send message : %s" % e)
