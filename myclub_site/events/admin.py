# \myclub_root\events\admin.py

from ast import AsyncFunctionDef
from django.contrib import admin
from .models import MySessions, MyVidPatterns, MyUser, Vidos, Chan, Mess, ST

from django.forms import TextInput, Textarea
from django.db import models

#class YourModelAdmin(admin.ModelAdmin):
#  formfield_overrides = {
#      models.CharField: {'widget': TextInput(attrs={'size':'20'})}, # ЕСЛИ ПОТРЕБУЕТСЯ ПЕРЕОПРЕДЕЛИТЬ НАПР. ЛОГ ПОД РАЗМЕР ПОЛЯ, ВИЗУАЛЬНО ПЕРЕДЕЛАТЬ, ТО ЭТО ТАК КАКТО.
#      models.TextField: {'widget': Textarea(attrs={'rows':100, 'cols':100})},
#  }

@admin.register(MyVidPatterns)
class MyVidPatternsAdmin(admin.ModelAdmin):
    list_display = ('vid_url_sub', 'vid_url_prefix', 'id_starts_at', 'vid_is_channel','vid_provider_name')

@admin.register(MyUser)
class MyUserAdmin(admin.ModelAdmin):
    list_display = ('telegram_id', 'username', 'downloading_now', 'waiting_channels_now', 'userIsEng', 'num_files_downloaded', 'mb_downloaded', 'gb_downloaded', 'max_gb_can_download', 'gb_has_now', 'max_gb_can_have', 'is_limited', 'max_connections_limit', 'when_started', 'when_last_activity', 'when_last_download', 'invited_people')

@admin.register(Vidos)
class VidosAdmin(admin.ModelAdmin):
    list_display = ('video_id', 'is_from_channel', 'bot_video_id', 'name', 'filename', 'he_downloaded', 'weight_mb', 'is_downloaded', 'when_started', 'when_requested', 'times_requested', 'is_part', 'of_parts', 'is_heavy', 'time_to_download_sec')

@admin.register(Chan)
class ChanAdmin(admin.ModelAdmin):
    list_display = ('name', 'he_started', 'last_vid', 'channel_id', 'when_started', 'when_last_vid', 'hours_to_refresh', 'avg_video_weight')

@admin.register(MySessions)
class MySessionsAdmin(admin.ModelAdmin):
    list_display = ('session_id', 'who_started', 'why_started', 'when_started')

@admin.register(Mess)
class MessAdmin(admin.ModelAdmin):
    list_display = ('he_sent', 'description', 'when_started')

@admin.register(ST)
class STAdmin(admin.ModelAdmin):
    list_display = ('date', 'num_new_users', 'num_files_requested', 'num_files_downloaded', 'gb_downloaded', 'gb_stored', 'files_stored')
