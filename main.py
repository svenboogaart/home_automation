from automation.brain import Brain
from database.data_layer import DataLayer
from database.migration import Migration
from hue.data_loader.api_v2.hue_contact_loader import HueContactLoaderV2
from hue.data_loader.hue_sensors_loader import HueSensorsLoader
from hue.handlers.hue_contact_handler import HueContactHandler
from hue.handlers.hue_daylight_sensor_handler import HueDaylightSensorHandler
from hue.handlers.hue_lights_handler import HueLightsHandler
from hue.handlers.hue_motion_sensor_handler import HueMotionSensorHandler
from hue.handlers.hue_switches_handler import HueSwitchesHandler
from hue.handlers.hue_temperature_sensor_handler import HueTemperatureSensorHandler
from hue.hue_connector import HueConnector
from hue.hue_connector_v2 import HueConnectorV2
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
    database_layer = DataLayer()

    hue_connection = HueConnector(settings)
    hue_sensor_loader = HueSensorsLoader(hue_connection)

    hue_lights_handler = HueLightsHandler(hue_connection)
    hue_motion_sensor_handler = HueMotionSensorHandler(hue_sensor_loader)
    hue_switches_handler = HueSwitchesHandler(hue_sensor_loader)
    hue_daylight_sensor_handler = HueDaylightSensorHandler(hue_sensor_loader)
    hue_temperature_sensor_handler = HueTemperatureSensorHandler(hue_sensor_loader)

    hue_connector = HueConnectorV2(settings)
    hue_contact_loader = HueContactLoaderV2(hue_connector)
    contact_handler = HueContactHandler(hue_contact_loader)

    audio_manager = AudioManager(settings)
    sms_manager = SmsManager(settings)
    mail_manager = MailManager(settings)

    lights_manager = LightsManager(hue_lights_handler)
    switches_manager = SwitchesManager(hue_switches_handler)
    motion_sensor_manager = MotionSensorManager(hue_motion_sensor_handler)

    brain = Brain(database_layer, lights_manager, switches_manager, motion_sensor_manager,
                  hue_temperature_sensor_handler, hue_daylight_sensor_handler, contact_handler, audio_manager,
                  sms_manager,
                  mail_manager, settings)

    migration = Migration()
    migration.migrate()
    brain.control_automation()
