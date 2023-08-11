from django.db import models


# Create your models here.

class LightCommands(models.Model):
    command = models.CharField("Executed command", max_length=256)
    date = models.DateTimeField("Date triggerd", auto_now_add=True)
