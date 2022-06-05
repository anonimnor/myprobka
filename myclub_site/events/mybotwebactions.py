# \myclub_root\events\mybotwebactions.py
# скрипт делает что-то с процессом бота:
# а) может отображать активность его, активен/нет, а может, дважды запущено? трижды?
# б) может убить его (и некоторые его вспомогательные процессы..)
# в) может запустить его. обычно после убийства делается, но я разделил.. на всякий случй..
# г) лог сохраняет / очищает / показывает..

from django.shortcuts import render
from django.http import HttpResponse
from calendar import HTMLCalendar
from datetime import datetime, timezone
import subprocess
from subprocess import check_output
import shlex
import time

def botkill(request):
    myresponse='KILLING BOT(s)..'
    mycommand = "/code/myclub_site/batchs/mybotkiller.sh"
    myargs=shlex.split(mycommand)
    p = subprocess.Popen(myargs, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
    output, errors = p.communicate()
    return render(request,
        'events/system_responses.html',
        {'response':myresponse,'output':output,'errors':errors},
    )

def botstart(request):
    myresponse='STARTING BOT...'
    mycommand = "/code/myclub_site/batchs/mybotstarter.sh &"
    myargs=shlex.split(mycommand)
    # p = subprocess.Popen(myargs, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
    check_output(mycommand, shell = True)
    output="maybe started.."
    errors='maybe no errors..'
    time.sleep(1) #почемуто сразу не успевает отрабатывать, а если здесь хавается return, то Popen прикрывается, не начавшись (т.к. процесс просто захлопнется).
    return render(request,
        'events/system_responses.html',
        {'response':myresponse,'output':output,'errors':errors},
    )

def botcheck(request):
    myresponse='LETS SEE THE PROCESSES BOTS...'
    mycommand = "/code/myclub_site/batchs/mybotmonitor.sh"
    myargs=shlex.split(mycommand)
    p = subprocess.Popen(myargs, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
    output, errors = p.communicate()
    return render(request,
        'events/system_responses.html',
        {'response':myresponse,'output':(str(output)),'errors':errors},
    )

def botlog(request):
    myresponse='LETS SEE THE BOT LOGS...'

    mycommand = "cat /code/myclub_site/BOT.txt"
    myargs=shlex.split(mycommand)
    p = subprocess.Popen(myargs, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
    output, errors = p.communicate()
    output0='\n\n--------- BOT LOG: \n'+output
    aname0='BOT'
    
    mycommand = "cat /code/myclub_site/CHANLOADER.txt"
    myargs=shlex.split(mycommand)
    p = subprocess.Popen(myargs, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
    output, errors = p.communicate()
    output1='\n\n--------- CHANLOADER.py LOG: \n'+output
    aname1='CHANLOADER'
    
    mycommand = "cat /code/myclub_site/HANDLER.txt"
    myargs=shlex.split(mycommand)
    p = subprocess.Popen(myargs, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
    output, errors = p.communicate()
    output2='\n\n--------- HANDLER.py LOG: \n'+output
    aname2='HANDLER'
    
    mycommand = "cat /code/myclub_site/ONEFORALL.txt"
    myargs=shlex.split(mycommand)
    p = subprocess.Popen(myargs, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
    output, errors = p.communicate()
    output3='\n\n--------- ONEFORALL.py LOG: \n'+output
    aname3='ONEFORALL'
    
    mycommand = "cat /code/myclub_site/USERSTARTMANAGER.txt"
    myargs=shlex.split(mycommand)
    p = subprocess.Popen(myargs, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
    output, errors = p.communicate()
    output4='\n\n--------- USERSTARTMANAGER.py LOG: \n'+output
    aname4='USERSTARTMANAGER'
    
    mycommand = "cat /code/myclub_site/VIDLOADER.txt"
    myargs=shlex.split(mycommand)
    p = subprocess.Popen(myargs, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
    output, errors = p.communicate()
    output5='\n\n--------- VIDLOADER.py LOG: \n'+output
    aname5='VIDLOADER'

    mycommand = "cat /code/myclub_site/VIDSENDER.txt"
    myargs=shlex.split(mycommand)
    p = subprocess.Popen(myargs, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
    output, errors = p.communicate()
    output6='\n\n--------- VIDSENDER.py LOG: \n'+output
    aname6='VIDSENDER'

    mycommand = "cat /code/myclub_site/VIDWAITER.txt"
    myargs=shlex.split(mycommand)
    p = subprocess.Popen(myargs, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
    output, errors = p.communicate()
    output7='\n\n--------- VIDWAITER.py LOG: \n'+output
    aname7='VIDWAITER'

    return render(request,
        'events/system_responses.html',
        {'response':myresponse,
	'aname0':aname0,
	'output0':output0,
	'aname1':aname1,
	'output1':output1,
	'aname2':aname2,
	'output2':output2,
	'aname3':aname3,
	'output3':output3,
	'aname4':aname4,
	'output4':output4,
	'aname5':aname5,
	'output5':output5,
	'aname6':aname6,
	'output6':output6,
	'aname7':aname7,
	'output7':output7,
	'errors':errors},
    )

def clearlog(request):
    myresponse='CLEARING BOTLOG...'
    mycommand = "/code/myclub_site/batchs/mylogkiller.sh"
    myargs=shlex.split(mycommand)
    p = subprocess.Popen(myargs, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
    output, errors = p.communicate()
    return render(request,
        'events/system_responses.html',
        {'response':myresponse,'output':output,'errors':errors},
    )

def mytest(request): #чтобы не городить в именах огород, - тестирует бота на работоспособность, если 1 или более запущено, - возвращает 1 иначе 0..
    myresponse='0'
    mycommand = "/code/myclub_site/batchs/mybotmonitor.sh"
    myargs=shlex.split(mycommand)
    p = subprocess.Popen(myargs, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
    output, errors = p.communicate()
    return render(request,
        'events/bot_status.html',
        {'output':output},
    )
