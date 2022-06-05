# \myclub_root\events\urls.py

from django.urls import path, re_path
from . import views
from . import mydbupdates
from . import mybotwebactions
from . import mystatistics
from . import myProbks

# urlpatterns = [
    # path('', views.index, name='index'),
#    path('<int:year>/<str:month>/', views.index, name='index'),
# ]

urlpatterns = [
    path('', views.index, name='index'),
    path('updateVidPatterns/', mydbupdates.updateVdiPatterns, name='updateVdiPatterns'),
    path('botkill/', mybotwebactions.botkill, name='botkill'),
    path('botstart/', mybotwebactions.botstart, name='botstart'),
    path('botcheck/', mybotwebactions.botcheck, name='botcheck'),
    path('botlog/', mybotwebactions.botlog, name='botlog'),
    path('clearlog/', mybotwebactions.clearlog, name='clearlog'),

    path('dailystats/', mystatistics.dailystats, name='dailystats'),
    path('userstats/', mystatistics.userstats, name='userstats'),
    path('vidstats/', mystatistics.vidstats, name='vidstats'),
    path('actionstats/', mystatistics.actionstats, name='actionstats'),
    path('gbstats/', mystatistics.gbstats, name='gbstats'),
    
    path('mytest/', mybotwebactions.mytest, name='mytest'),
    
    path('events/', views.all_events, name='show-events'),
    path('myprobks/', myProbks.probkShowHTML, name='myprobkshtml'),
    path('myprobksjson/', myProbks.probkShowJson, name='myprobksjson'),
    
    # path('<int:year>/<str:month>/', views.index, name='index'),
    #  re_path(r'^(?P<year>[0-9]{4})/(?P<month>0?[1-9]|1[0-2])/', views.index, name='index'),
    re_path(r'^(?P<year>[0-9]{4})/(?P<month>0?[1-9]|1[0-2])/', views.index, name='index'),
]