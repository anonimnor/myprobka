# \myclub_root\events\myprobksCheck.py
# скрипт пока отображает хоть чегото.
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

