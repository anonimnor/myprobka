# \myclub_root\events\models.py
# файл моделей для Django базы, - пока здесь пусто, бд проект не подразумевает..

from pickle import TRUE
from django.db import models
from django.contrib.auth.models import User

class MyUser(models.Model): # пользовательский класс..
    username = models.CharField('User Nik', default='Some User', max_length=30, help_text="Никнейм (необязателен)")
    def __str__(self):
        return str(self.username)
