# \myclub_root\events\myGraphBuilder.py
# скрипт для отображения форм на построение графов, - вся информация в шаблоне, поэтому скрипт пустой.

from django.shortcuts import render
from django.http import HttpResponse
from django.dispatch import receiver
from django.db.models.signals import post_save

def showHTML(request):
    mymess="{test}"
    context = {
        'mymess': mymess,
    }
    return render(request,
        'events/graphBuilder.html',
        context=context
    )

