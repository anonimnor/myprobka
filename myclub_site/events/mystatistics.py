# \myclub_root\events\mystatistics.py
# скрипт отображает статистику.
# ...сколько сегодня зарегано,
# ...сколько сегодня пользовалось,
# ...сколько сегодня файлов скачалось,
# ...сколько сегодня суммарно гб скачалось,
# ...сколько сегодня суммарно гб в хранилище...
# ...сколько сегодня суммарно файлов в хранилище...
# както так..чтоль....

from ast import AsyncFunctionDef
from django.shortcuts import render
from django.http import HttpResponse
from calendar import HTMLCalendar
from datetime import datetime, timezone, timedelta
import subprocess
from subprocess import check_output
from events.models import MyUser, Vidos, ST
from django.utils.timezone import now
from django.db.models import Sum, F
import shlex
import time

def dailystats(request):
    mydailystats = ST.objects.all().order_by('-date')[0:15]
    myNumActiveUsers=[]
    myNumTotalUsers=[]
    userGrowth=0
    for statdate in mydailystats:
        # statdate.num_files_requested=Vidos.objects.filter(when_requested__date=statdate.date.date()).count() # нельзя: переезжает дата запрошенного файла наперёд.
        statdate.num_files_downloaded=Vidos.objects.filter(when_started__date=statdate.date.date()).count()
        gb=Vidos.objects.filter(when_started__date=statdate.date.date()).aggregate(Sum('weight_mb')) # returns {'weight_mb__sum': 1000} for example
        if(gb):
            if(gb['weight_mb__sum']==None):
                gb=1
            else:
                gb=int(int(gb['weight_mb__sum'])/1024)
        else:
            gb=1
        statdate.gb_downloaded=gb
        statdate.save()
        myNumActiveUsers.append(statdate.active_users.count())
        myNumTotalUsers.append(MyUser.objects.all().count()-userGrowth)
        userGrowth+=statdate.num_new_users

    return render(request,
        'events/statistics_template.html',
        {'mydailystats': mydailystats,
        'statname': 'ЗА 10 ПОСЛЕДНИХ ДНЕЙ:',
        'myNumActiveUsers': myNumActiveUsers,
        'myNumTotalUsers': myNumTotalUsers,
        }
    )    

def userstats(request):
    myusers = MyUser.objects.all().order_by('-gb_downloaded')[0:15]
    return render(request,
        'events/bagel_template.html',
        {'mything': myusers,
        'statname': 'ПОЛЬЗОВАТЕЛИ ПО ВЕСУ:',
        'maxnum': 15
        }
    )    

def vidstats(request):
    mything_weight = Vidos.objects.all().order_by('-weight_mb','video_id').distinct('weight_mb','video_id')[0:15]
    mything_activity = Vidos.objects.all().order_by('-times_requested','video_id').distinct('times_requested','video_id')[0:15]
    mything_longwait = Vidos.objects.all().order_by('-time_to_download_sec','video_id').distinct('time_to_download_sec','video_id')[0:15]
    mything_recent = Vidos.objects.all().order_by('-when_requested','video_id').distinct('when_requested','video_id')[0:15]
    return render(request,
        'events/bagel_template_v.html',
        {
            'mything_weight': mything_weight,
            'mything_longwait': mything_longwait,
            'mything_activity': mything_activity,
            'mything_recent': mything_recent,
            'statname': 'ФАЙЛЫ ВИДЕО:',
            'maxnum': 15
        }
    )    

def gbstats(request):
    myvideos = Vidos.objects.all().order_by('weight_mb')[0:10]
    return render(request,
        'events/bagel_template.html',
        {'mything': myvideos,
        'statname': 'ПОКА НЕ РАБОТАЕТ.'
        }
    )    

def actionstats(request):
    myvideos = Vidos.objects.all().order_by('weight_mb')[0:10]
    return render(request,
        'events/bagel_template.html',
        {'mything': myvideos,
        'statname': 'ПОКА НЕ РАБОТАЕТ.'
        }
    )    
