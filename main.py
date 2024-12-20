from automation.brain import Brain
from database.DataLayer import DataLayer
from database.migration import Migration
from hue.hue_connector import HueConnector
from hue.lights.hue_lights_handler import HueLightsHandler
from hue.sensors.hue_sensors_manager import HueSensorsManager
from hue.sensors.hue_switches_handler import HueSwitchesHandler

from models.managers.audio_manager import AudioManager
from models.managers.lights_manager import LightsManager
from models.managers.mail_manager import MailManager
from models.managers.motion_sensor_manager import MotionSensorManager
from models.managers.sms_manager import SmsManager
from models.managers.switches_manager import SwitchesManager
from settings.settings import Settings

if __name__ == '__main__':
    print("Starting home automation")
    settings = Settings()
    hue_connection = HueConnector(settings)
    database_layer = DataLayer()
    hue_lights_handler = HueLightsHandler(hue_connection, database_layer)
    sensor_manager = HueSensorsManager(hue_connection)
    hue_switches_handler = HueSwitchesHandler(sensor_manager)
    audio_manager = AudioManager(settings)
    sms_manager = SmsManager(settings)
    mail_manager = MailManager(settings)

    lights_manager = LightsManager(hue_lights_handler)
    switches_manager = SwitchesManager(hue_switches_handler)
    motion_sensor_manager = MotionSensorManager(sensor_manager)

    brain = Brain(database_layer, lights_manager, switches_manager, motion_sensor_manager, audio_manager, sms_manager,
                  mail_manager, settings)

    migration = Migration()
    migration.migrate()
    brain.control_automation()
