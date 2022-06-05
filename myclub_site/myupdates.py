#!/usr/bin/env python3
# \myclub_site\myupdates.py

import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myclub_site.settings')
import django
django.setup() # это команда ПЕРЕОПРЕДЕЛЯЕТ djanog WEB-фреймворк на НЕ-WEB использование. и должна видимо быть вызвана до импорта чат-класса (он с БД). дело в том что из web мы запустить бота не можем, - он в вечном цикле, только fork если разве что...

import events.mydbupdates
events.mydbupdates.updateVP()