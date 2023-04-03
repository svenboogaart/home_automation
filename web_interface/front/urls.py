from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("light/<str:light_id>/on", views.light_on),
    path("light/<str:light_id>/off", views.light_of),
    path("lights-off", views.lights_off, name="index"),
    path("lights-on", views.lights_on, name="index"),
]