from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("lights-off", views.lights_off, name="index"),
    path("lights-on", views.lights_on, name="index"),
]