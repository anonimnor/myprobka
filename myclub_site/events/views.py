# \myclub_root\events\views.py
from django.shortcuts import render
from django.http import HttpResponse
from datetime import date

def index(request, year=date.today().year, month=date.today().month):
    return HttpResponse("<h1>PROBKS</h1><p>nothing in index. use proper urls.</p>")
