from django.db import models
from datetime import datetime
from news.models import *
 
 
# class Appointment(models.Model): # модель записи - сообщение от пользователя, его имя и дата записи
#     date = models.DateField(
#         default=datetime.utcnow,
#     )
#     client_name = models.CharField(
#         max_length=200
#     )
#     message = models.TextField()
 
#     def __str__(self):
#         return f'{self.client_name}: {self.message}'


class Appointment(models.Model): # модель записи - сообщение от пользователя, его имя и дата записи
    date = models.DateField(
        default=datetime.utcnow,
    )
    client_name = models.CharField(
        max_length=200
    )
    message = models.TextField()
 
    def __str__(self):
        return f'{self.client_name}: {self.message}'