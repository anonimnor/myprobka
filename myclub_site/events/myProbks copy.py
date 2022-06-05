# \myclub_root\events\myProbks.py
# скрипт пока отображает хоть чегото.

from calendar import c
from django.shortcuts import render
from django.http import HttpResponse
from PIL import Image
from PIL import ImageDraw
from django.dispatch import receiver
from django.db.models.signals import post_save
import base64
from io import BytesIO
import math
import random
import json
import requests
import logging

logger = logging.getLogger('myLogger')
logger.setLevel(level=logging.INFO)
fh=logging.FileHandler('myProbkas.log',mode='w+')
fh.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
fh.setLevel(level=logging.INFO)
logger.addHandler(fh)
logger.info('---------------- init of myProbks.py at myProbkas.log -----------------')

class myImage:
    def arrowedLine(self, ptA, ptB, width=10, color=(0,255,0), outline='#000000'):
        """Draw line from ptA to ptB with arrowhead at ptB and arrowhollow at ptA, of width, color and outline,
        returns updated image"""
        width = width*(self.xScale+self.yScale)/2
        xA, yA = ptA
        xB, yB = ptB
        xA = (xA - self.xStart)*self.xScale
        xB = (xB - self.xStart)*self.xScale
        yA = (yA - self.yStart)*self.yScale
        yB = (yB - self.yStart)*self.yScale
        angle = math.atan2(xB-xA,yB-yA)
        sin = math.sin(angle)
        cos = math.cos(angle)
        ptAN = xA+width*sin, yA+width*cos
        ptA1 = xA+width*cos, yA-width*sin
        ptB1 = xB-width*sin+width*cos, yB-width*cos-width*sin
        ptB2 = xB-width*sin-width*cos, yB-width*cos+width*sin
        ptA2 = xA-width*cos, yA+width*sin
        ptB = xB, yB
        self.draw.polygon([ptAN, ptA1, ptB1, ptB, ptB2, ptA2], fill=color, outline=outline)
        # self.draw.line((ptA, ptB), fill='red') # - контроль, проверка...
        return self.img

    def circle(self, ptA, width=0.001, color=(255,0,0), outline='#000000'):
        """Draw circle at ptA, of width with color and outline, 
        returns updated image"""
        width = width*(self.xScale+self.yScale)/2
        ptAx, ptAy = ptA
        ptAx = (ptAx - self.xStart)*self.xScale
        ptAy = (ptAy - self.yStart)*self.yScale
        ptA1 = ptAx - width/2
        ptA2 = ptAy - width/2
        ptA3 = ptAx + width/2
        ptA4 = ptAy + width/2
        self.draw.ellipse([int(ptA1), int(ptA2), int(ptA3), int(ptA4)], fill=color, outline=outline)
        logger.info(' circle drawn, %s ',[ptA1, ptA2, ptA3, ptA4, self.xScale, self.yScale])
        return self.img

    def __init__(self, width, height, xScale, yScale, minGeo, maxGeo, midGeo):
        self.xScale=xScale
        self.yScale=yScale
        self.xStart=minGeo[0]
        self.yStart=minGeo[1]

        self.img=Image.open('https://static-maps.yandex.ru/1.x/?ll='+str(midGeo[1])+','+str(midGeo[0])+'&z=15&l=map&size=650,450') # пока статичный;
        newSize = int(width*0.027466/(maxGeo[0]-minGeo[0])), int(width*0.010919/(maxGeo[1]-minGeo[1]))
        self.img = self.img.resize(newSize, resample=Image.LANCZOS) # получили карту из яндекса в нужных нам пропорциях.. теперь ставим её по центру нашей картинки и подрезаем по её границам..
        offset = int((width-newSize[0])/2), int((height-newSize[1])/2)
        self.img=Image.new("RGB", (int(width), int(height))).paste(self.img, offset) # paste в bg, offset = (bg_w-im_w)/2

        self.draw = ImageDraw.Draw(self.img)
        logger.info('............. init of myImage class %s -----------------',str(midGeo))

def probkShowJson(request): # удалить потом, ненужная функция...
    jsOnCode='{test}'
    return HttpResponse(jsOnCode, content_type='application/json')

def probkShowHTML(request):

    def getMinMaxCoords(allNodes):
        """of [10,10], [20,50], [100,40] - returns [10,10],[100,50] boundaries"""
        if(allNodes):
            minX, minY = allNodes[0]
            maxX, maxY = allNodes[0]
            for node in allNodes:
                if(minX>node[0]):
                    minX=node[0]
                if(minY>node[1]):
                    minY=node[1]
                if(maxX<node[0]):
                    maxX=node[0]
                if(maxY<node[1]):
                    maxY=node[1]
            midX = (maxX - minX)/2 + minX
            midY = (maxY - minY)/2 + minY
            return [minX, minY], [maxX, maxY], [midX, midY]
        else:
            return [0,0],[0,0]

    logger.info(' =============== init of probkShowHTML! =============== ')

    # response = requests.get("https://mob-aks.com/graph.json")
    response = requests.get("https://mob-aks.com/graphFull.json")
    myJsOn = json.loads(response.text)

    preResampleScale = 2.5 # от начального масштаба зависит уровень сглаживания (чем больше тут число, тем глаже, - но медленнее..)
    resampleMethod=Image.LANCZOS # от этого тоже зависит; здесь возможны - LANCZOS, BILINEAR.. BICUBIC, ещё что-то возможно... (LANCZOS видимо самый медленный...)
    imgW, imgH = preResampleScale * myJsOn["image"]['width'], preResampleScale * myJsOn["image"]['height'] # юзаем увеличенную карту, потом сожмём для anti-aliasing сглаживания..
    imgWR, imgHR = myJsOn["image"]['width'], myJsOn["image"]['height']
    
    allNodesGeo=[] # соберём все точки Geo-координат lng/lat, чтоб границы зоны очертить... (представлено вида 55.7389525936213 = lat = Y, 37,61455801 = lng = X)
    allNodesOur=[] # а так же и точки в неясной системе координат, представленные как 4188783.732476062 (недо-UTM какаято...)
    
    myNodes=myJsOn["graph"]['nodes']
    myLinks=myJsOn["graph"]['links']
    myLoads=myJsOn["loads"]

    # LAT - LATITUDE - ШИРОТА - угол между макушкой чоловека и плоскостью экватора (на экваторе = 0, вниз от экватора - отрицательное, вверх - положительное, до 90с градусов)
    # ДЛЯ НАС ШИРОТА ЭТО YY-координата, причём чем больше, тем ВЫШЕ точка.
    
    # LNG - LONGITUDE - ДОЛГОТА, угол между гринвичевским меридианом и меридианом, проходящим через макушку человека; к востоку - положителен, до 180c градусов)
    # ДЛЯ НАС ДОЛГОТА ЭТО XX-координата, причём чем больше, тем ПРАВЕЕ точка.
    
    if myNodes:
        for node in myNodes:
            allNodesGeo.append([node["location"]["lng"], node["location"]["lat"]])
            if(node["geometry"]["center"]):
                allNodesOur.append(node["geometry"]["center"])
    if myLinks:
        for link in myLinks:
            allNodesGeo.append([link["startPoint"]["lng"], link["startPoint"]["lat"]])
            allNodesGeo.append([link["endPoint"]["lng"], link["endPoint"]["lat"]])
            if(link["geometry"]['coordinates']):
                for coords in link["geometry"]['coordinates']:
                    allNodesOur.append(coords)
    
    minGeo, maxGeo, midGeo = getMinMaxCoords(allNodesGeo)
    minOur, maxOur, midOur = getMinMaxCoords(allNodesOur)

    # вычисляем коэффициенты сжатия для карты, исходя из min/max и размеров карты...
    xScaleGeo=imgW/(maxGeo[0]-minGeo[0])
    yScaleGeo=imgH/(maxGeo[1]-minGeo[1])
    xScaleOur=imgW/(maxOur[0]-minOur[0])
    yScaleOur=imgH/(maxOur[1]-minOur[1])
    # теперь достаточно помножить (X-minX) или (Y-minY) точки на этот scale, 
    # чтоб получить её координаты на картинке...
    
    myImageGeo = myImage(imgW, imgH, xScaleGeo, yScaleGeo, minGeo, maxGeo, midGeo)
    myImageOur = myImage(imgW, imgH, xScaleOur, yScaleOur, minOur, maxOur, midOur)

    mymess=str(myImageGeo.xStart)+" : "+str(myImageGeo.xScale)
    
    if(myLinks):
        for link in myLinks:
            # 0-2 - зеленый, 3-6 - желтый, 6-9 - красный, 10 - бордовый, нет данных - серый:
            myColor='gray'
            if(myLoads):
                for load in myLoads:
                    if(load["link_id"]==link["id"]):
                        if(load["load"]>=10):
                            myColor='#aa0000'
                        if(load["load"]<10):
                            myColor='#ff0000'
                        if(load["load"]<6):
                            myColor='#ffaa00'
                        if(load["load"]<3):
                            myColor='green'
                        break
            myImageGeo.arrowedLine([link["startPoint"]["lng"], link["startPoint"]["lat"]], [link["endPoint"]["lng"], link["endPoint"]["lat"]], 0.00017, myColor)
            if(link["geometry"]['coordinates']):
                prevCoords=link["geometry"]['coordinates'][0]
                for coords in link["geometry"]['coordinates']:
                    if(coords==prevCoords):
                        pass # их по крайней мере две...
                    else:
                        myImageOur.arrowedLine(prevCoords, coords, 26, myColor)
                        prevCoords=coords

    if(myNodes):
        for node in myNodes:
            myImageGeo.circle([node["location"]["lng"], node["location"]["lat"]], 0.000007*node["geometry"]["radius"], 'red')
            if(node["geometry"]["center"]):
                myImageOur.circle(node["geometry"]["center"], node["geometry"]["radius"], 'red')

    myImageGeo.img = myImageGeo.img.resize((imgWR, imgHR), resample=resampleMethod)
    myImageOur.img = myImageOur.img.resize((imgWR, imgHR), resample=resampleMethod)

    img_file_geo = BytesIO()
    myImageGeo.img.save(img_file_geo,format="PNG")
    img_file_our = BytesIO()
    myImageOur.img.save(img_file_our,format="PNG")
   
    context = {
        'img_str_geo': base64.b64encode(img_file_geo.getvalue()).decode('utf-8'),
        'img_str_our': base64.b64encode(img_file_our.getvalue()).decode('utf-8'),
        'mymess': mymess,
    }
    return render(request,
        'events/probks_template.html',
        context=context
    )

