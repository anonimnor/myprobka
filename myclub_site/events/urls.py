# \myclub_root\events\urls.py

from django.urls import path, re_path
from . import views
from . import myProbks
from . import myprobksCheck
from . import myprobksSender
# from . import myprobksJson
from . import myprobksJsonTest
from . import myGraphBuilder
from . import myOneGraphBuilder

urlpatterns = [
    path('', views.index, name='index'),
    
    path('probkShowJson/', myProbks.probkShowJson, name='myprobkshowjson'),
    path('probkShowHtml/', myProbks.probkShowHtml, name='myprobkshowhtml'),
    path('probkShowJsonFromUrl/', myProbks.probkShowJsonFromUrl, name='probkshowjsonfromurl'), # запросы вида http://localhost:8003/probkShowHtmlFromUrl/?URL=https://www.mob-aks.com/graphFull.json
    path('probkShowHtmlFromUrl/', myProbks.probkShowHtmlFromUrl, name='probkshowhtmlfromurl'), # запросы вида http://localhost:8003/probkShowHtmlFromUrl/?URL=https://www.mob-aks.com/graphFull.json

    path('myprobksCheck/', myprobksCheck.probkShowHTML, name='myprobkscheck'),
    path('myprobksSender/', myprobksSender.probkShowHTML, name='myprobkssender'),
    path('myprobksJsonTest/', myprobksJsonTest.probkShowHTML, name='myprobksjsontest'),
    path('myGraphBuilder/', myGraphBuilder.showHTML, name='mygraphbuilder'),
    path('myOneGraphBuilder/', myOneGraphBuilder.showHTML, name='myonegraphbuilder'),
]