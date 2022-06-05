#!/usr/bin/env python3
# \myclub_site\myProbka.py
# скрипт пока не нужен

from PIL import Image
from PIL import ImageDraw
import json
import requests

response = requests.get("https://mob-aks.com/graph.json")
myGraph = json.loads(response.text)
print('вот граф...')
print(myGraph)

# print('вот парс...')
# for myParse in myGraph:
#    if(myParse[""])

