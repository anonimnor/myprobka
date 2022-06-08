# \myclub_root\events\myprobksSender.py
# проверочный микроскрипт, отображает {test}; в дальнейшем предполагается использовать для отправки графов с пробками..

from django.shortcuts import render
from django.http import HttpResponse
from django.dispatch import receiver
from django.db.models.signals import post_save

def probkShowHTML(request):
    mymess="{test}"
    context = {
        'mymess': mymess,
    }
    return render(request,
        'events/probksSender_template.html',
        context=context
    )

