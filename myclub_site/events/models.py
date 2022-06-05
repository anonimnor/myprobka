# \myclub_root\events\models.py

from pickle import TRUE
from django.db import models
from django.contrib.auth.models import User

class MyUser(models.Model): 
    username = models.CharField('User Nik', default='Some User', max_length=30, help_text="Никнейм (необязателен)")
    def __str__(self):
        return str(self.username)
