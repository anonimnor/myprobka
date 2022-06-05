# \myclub_root\events\admin.py

from ast import AsyncFunctionDef
from django.contrib import admin
from .models import MyUser

from django.forms import TextInput, Textarea
from django.db import models

#class YourModelAdmin(admin.ModelAdmin):
#  formfield_overrides = {
#      models.CharField: {'widget': TextInput(attrs={'size':'20'})}, # ЕСЛИ ПОТРЕБУЕТСЯ ПЕРЕОПРЕДЕЛИТЬ НАПР. ЛОГ ПОД РАЗМЕР ПОЛЯ, ВИЗУАЛЬНО ПЕРЕДЕЛАТЬ, ТО ЭТО ТАК КАКТО.
#      models.TextField: {'widget': Textarea(attrs={'rows':100, 'cols':100})},
#  }

@admin.register(MyUser)
class MyUserAdmin(admin.ModelAdmin):
    list_display = ('username',)


