# \myclub_root\events\urls.py

from django.urls import path, re_path
from . import views
from . import mydbupdates
from . import mybotwebactions
from . import mystatistics
from . import myProbks
from . import myprobksCheck

# urlpatterns = [
    # path('', views.index, name='index'),
#    path('<int:year>/<str:month>/', views.index, name='index'),
# ]

urlpatterns = [
    path('', views.index, name='index'),
    path('myprobks/', myProbks.probkShowHTML, name='myprobkshtml'),
    path('myprobksCheck/', myprobksCheck.probkShowHTML, name='myprobkscheck'),
    path('myprobksjson/', myProbks.probkShowJson, name='myprobksjson'),
    
    # path('<int:year>/<str:month>/', views.index, name='index'),
    #  re_path(r'^(?P<year>[0-9]{4})/(?P<month>0?[1-9]|1[0-2])/', views.index, name='index'),
    re_path(r'^(?P<year>[0-9]{4})/(?P<month>0?[1-9]|1[0-2])/', views.index, name='index'),
]