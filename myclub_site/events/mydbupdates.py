# \myclub_root\events\mydpupdates.py
# скрипт очищает MyVidPatterns из DB, затем пишет туда, чего трэба. - фиксированные значения для паттернов. 
# СКРИПТ ТРЕБУЕТСЯ ЗАПУСКАТЬ!! - url /updateVidPatterns/
# СКРИПТ СОДЕРЖИТ ВНИЗУ ТАМ В КОММЕНТАРИХ - ХЕЛП ПО ДБ подсказки.

from django.shortcuts import render
from django.http import HttpResponse
from datetime import date
import calendar
import time
from calendar import HTMLCalendar
from datetime import datetime, timezone

from events.models import MyVidPatterns

def updateVP():
    MyVidPatterns.objects.all().delete()       
    MyVidPatterns.objects.create(vid_url_sub="p://www.youtu.be",vid_url_prefix='https://www.youtube.com/watch?v=',id_starts_at=20,vid_is_channel=False,vid_provider_name='YouTube')
    MyVidPatterns.objects.create(vid_url_sub="s://www.youtu.be",vid_url_prefix='https://www.youtube.com/watch?v=',id_starts_at=21,vid_is_channel=False,vid_provider_name='YouTube')
    MyVidPatterns.objects.create(vid_url_sub="p://youtu.be",vid_url_prefix='https://www.youtube.com/watch?v=',id_starts_at=16,vid_is_channel=False,vid_provider_name='YouTube')
    MyVidPatterns.objects.create(vid_url_sub="s://youtu.be",vid_url_prefix='https://www.youtube.com/watch?v=',id_starts_at=17,vid_is_channel=False,vid_provider_name='YouTube')
    MyVidPatterns.objects.create(vid_url_sub="p://m.youtube.com/shorts",vid_url_prefix='https://www.youtube.com/watch?v=',id_starts_at=28,vid_is_channel=False,vid_provider_name='YouTube')
    MyVidPatterns.objects.create(vid_url_sub="s://m.youtube.com/shorts",vid_url_prefix='https://www.youtube.com/watch?v=',id_starts_at=39,vid_is_channel=False,vid_provider_name='YouTube')
    MyVidPatterns.objects.create(vid_url_sub="p://m.youtube.com/watch",vid_url_prefix='https://www.youtube.com/watch?v=',id_starts_at=29,vid_is_channel=False,vid_provider_name='YouTube')
    MyVidPatterns.objects.create(vid_url_sub="s://m.youtube.com/watch",vid_url_prefix='https://www.youtube.com/watch?v=',id_starts_at=30,vid_is_channel=False,vid_provider_name='YouTube')
    MyVidPatterns.objects.create(vid_url_sub="p://youtube.com/shorts",vid_url_prefix='https://www.youtube.com/watch?v=',id_starts_at=26,vid_is_channel=False,vid_provider_name='YouTube')
    MyVidPatterns.objects.create(vid_url_sub="s://youtube.com/shorts",vid_url_prefix='https://www.youtube.com/watch?v=',id_starts_at=27,vid_is_channel=False,vid_provider_name='YouTube')
    MyVidPatterns.objects.create(vid_url_sub="p://www.youtube.com/shorts",vid_url_prefix='https://www.youtube.com/watch?v=',id_starts_at=30,vid_is_channel=False,vid_provider_name='YouTube')
    MyVidPatterns.objects.create(vid_url_sub="s://www.youtube.com/shorts",vid_url_prefix='https://www.youtube.com/watch?v=',id_starts_at=31,vid_is_channel=False,vid_provider_name='YouTube')
    MyVidPatterns.objects.create(vid_url_sub="p://youtube.com/watch",vid_url_prefix='https://www.youtube.com/watch?v=',id_starts_at=27,vid_is_channel=False,vid_provider_name='YouTube')
    MyVidPatterns.objects.create(vid_url_sub="s://youtube.com/watch",vid_url_prefix='https://www.youtube.com/watch?v=',id_starts_at=28,vid_is_channel=False,vid_provider_name='YouTube')
    MyVidPatterns.objects.create(vid_url_sub="p://www.youtube.com/watch",vid_url_prefix='https://www.youtube.com/watch?v=',id_starts_at=31,vid_is_channel=False,vid_provider_name='YouTube')
    MyVidPatterns.objects.create(vid_url_sub="s://www.youtube.com/watch",vid_url_prefix='https://www.youtube.com/watch?v=',id_starts_at=32,vid_is_channel=False,vid_provider_name='YouTube')
    MyVidPatterns.objects.create(vid_url_sub="p://www.youtube.com/channel",vid_url_prefix='https://www.youtube.com/feeds/videos.xml?channel_id=',id_starts_at=31,vid_is_channel=True,vid_provider_name='YouTube')
    MyVidPatterns.objects.create(vid_url_sub="s://www.youtube.com/channel",vid_url_prefix='https://www.youtube.com/feeds/videos.xml?channel_id=',id_starts_at=32,vid_is_channel=True,vid_provider_name='YouTube')
    MyVidPatterns.objects.create(vid_url_sub="p://m.youtube.com/channel",vid_url_prefix='https://www.youtube.com/feeds/videos.xml?channel_id=',id_starts_at=29,vid_is_channel=True,vid_provider_name='YouTube')
    MyVidPatterns.objects.create(vid_url_sub="s://m.youtube.com/channel",vid_url_prefix='https://www.youtube.com/feeds/videos.xml?channel_id=',id_starts_at=30,vid_is_channel=True,vid_provider_name='YouTube')
    MyVidPatterns.objects.create(vid_url_sub="p://youtube.com/channel",vid_url_prefix='https://www.youtube.com/feeds/videos.xml?channel_id=',id_starts_at=27,vid_is_channel=True,vid_provider_name='YouTube')
    MyVidPatterns.objects.create(vid_url_sub="s://youtube.com/channel",vid_url_prefix='https://www.youtube.com/feeds/videos.xml?channel_id=',id_starts_at=28,vid_is_channel=True,vid_provider_name='YouTube')


def updateVdiPatterns(request):
    myresponse='UPDATING MYVIDPATTERNS IN DB..'
    time.sleep(3) # анти-спам; вообще-то, здесь должна бы быть проверка на авторизованность..  

    updateVP()

    myresponse+=" MYVIDPATTERNS UPDATED OK IN DB."

    return render(request,
        'events/system_responses.html',
        {'response':myresponse}
    )
