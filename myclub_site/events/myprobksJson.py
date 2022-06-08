# \myclub_root\events\myprobksJson.py
# проверочный микроскрипт, отображает то, что в него отправлено..
from django.shortcuts import render
from django.http import HttpResponse
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.views.decorators.csrf import csrf_exempt # запрет на crsf-защиту; мы с разных сайтов получаем post, а токены не используем (пока нет в тз)

@csrf_exempt
def probkShowHTML(request):
    mymess=""+request.body.decode('UTF-8') # .body чтоль тут.. неуверен! (
    context = {
        'mymess': mymess,
    }
    return render(request,
        'events/probksCheck_template.html',
        context=context
    )

