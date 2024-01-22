from django.db import models
import datetime

# Create your models here.
class Room(models.Model):
    name = models.CharField(max_length=30)

    def __str__(self):
        return f'Комнатка {self.id} Название {self.name}'

class Message(models.Model):
    text = models.CharField(max_length=1000)
    room = models.CharField(max_length=30)
    date = models.DateTimeField(default=datetime.datetime.now())
    user = models.CharField(max_length=30)

    
