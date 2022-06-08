#!/usr/bin/env python3
# \myclub_site\myupdates.py

import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myclub_site.settings')
import django
django.setup() # это команда ПЕРЕОПРЕДЕЛЯЕТ djanog WEB-фреймворк на НЕ-WEB использование.

import events.mydbupdates
events.mydbupdates.updateVP()