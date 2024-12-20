import os
import sys
import threading
from threading import Thread
from playsound import playsound
from settings.settings import Settings


class AudioManager:

    @staticmethod
    def play_audio_file(file_path: str):
        def play_audio_file_threaded():
            try:
                if os.path.isfile(file_path):
                    playsound(file_path)
                else:
                    print("Failed to play audo, %s file not found " % file_path)
            except Exception as e:
                print("Failed to send message : %s" % e)
        thread = threading.Thread(target=play_audio_file_threaded)
        thread.start()

    def __init__(self, settings: Settings):
        self.__settings = settings

    def play_alarm_sound(self):
        if self.__settings.alarm_play_sound:
            self.play_audio_file(self.__settings.mp3_file_alarm)

    def play_activated_sound(self):
        self.play_audio_file(self.__settings.mp3_path_activated)

    def play_deactivate_sound(self):
        self.play_audio_file(self.__settings.mp3_path_deactivated)

    @staticmethod
    def say_something(text_to_say: str):
        if sys.platform.startswith('win'):
            Thread(target=os.system, args=("say \'%s\'" % text_to_say,)).start()
        elif sys.platform.startswith('linux'):
            Thread(target=os.system, args=("spd-say \'%s\'" % text_to_say,)).start()
        else:
            print("Text to speach not supported for os")
