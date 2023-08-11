import sys

from django.shortcuts import render, redirect

from database.DataLayer import DataLayer
from hue.lights.hue_lights_handler import HueLightsHandler
from hue.sensors.hue_sensors_manager import HueSensorsManager

sys.path.append('/Users/Sven/Documents/programming/python/home_automation')


from hue.hue_connector import HueConnector

hue_connector = HueConnector()
data_later = DataLayer()
sensor_manager = HueSensorsManager(hue_connector)
lights_manager = HueLightsHandler(hue_connector, data_later)



def index(request):
    print(lights_manager.get_lights())
    lights = lights_manager.get_lights()
    switches = sensor_manager.get_switches()
    return render(request, 'web_interface/index.html', {'lights': lights, 'switches': switches})


def lights_on(request):

    print(lights_manager.turn_all_lights_on())
    return redirect('/')

def lights_off(request):

    print(lights_manager.turn_all_lights_off())
    return redirect('/')

def light_on(request, light_id):
    lights_manager.set_light_on_state(light_id, "true")
    return redirect('/')

def light_warning(request, light_id):
    lights_manager.alarm_light(light_id, 0.2, 1.4, 5)
    return redirect('/')

def light_of(request, light_id):
    lights_manager.set_light_on_state(light_id, "false")
    return redirect('/')