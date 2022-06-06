# \myclub_root\events\myProbks.py
# скрипт пока отображает хоть чегото.

from calendar import c
from django.shortcuts import render
from django.http import HttpResponse
from PIL import Image, ImageOps, ImageDraw
from django.dispatch import receiver
from django.db.models.signals import post_save
import base64
from io import BytesIO
import math, random
import json, requests
import logging
import time
import os
import re
from django.views.decorators.csrf import csrf_exempt # запрет на crsf-защиту; мы с разных сайтов получаем post, а токены не используем (пока нет в тз)

logger = logging.getLogger('myLogger')
logger.setLevel(level=logging.INFO)
fh=logging.FileHandler('myProbkas.log',mode='w+')
fh.setFormatter(logging.Formatter('%(asctime)s - %(message)s - %(name)s - %(levelname)s'))
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
        ptAN = xA+width*sin, self.picHeight-(yA+width*cos) # здесь и далее все Y-координаты транспонированы! т.к. глобальная гео-ось Y перевёрнута, идёт сверху-вниз.
        ptA1 = xA+width*cos, self.picHeight-(yA-width*sin)
        ptB1 = xB-width*sin+width*cos, self.picHeight-(yB-width*cos-width*sin)
        ptB2 = xB-width*sin-width*cos, self.picHeight-(yB-width*cos+width*sin)
        ptA2 = xA-width*cos, self.picHeight-(yA+width*sin)
        ptB = xB, self.picHeight-yB
        self.draw.polygon([ptAN, ptA1, ptB1, ptB, ptB2, ptA2], fill=color, outline=outline)
        # self.draw.line((ptA, ptB), fill='red') # - тонкая линия красная - для контроля, проверка...
        return self.img

    def circle(self, ptA, width=0.001, color=(255,0,0), outline='#000000'):
        """Draw circle at ptA, of width with color and outline, 
        returns updated image"""
        logger.info(' circle drawing, %s ',[ptA, width, self.xScale, self.yScale, self.xStart, self.yStart])
        width = width*(self.xScale+self.yScale)/2
        ptAx, ptAy = ptA
        ptAx = (ptAx - self.xStart)*self.xScale
        ptAy = self.picHeight-((ptAy - self.yStart)*self.yScale)  # здесь и далее Y-координата транспонирована! т.к. глобальная гео-ось Y перевёрнута, идёт сверху-вниз.
        ptA1 = ptAx - width/2
        ptA2 = ptAy - width/2
        ptA3 = ptAx + width/2
        ptA4 = ptAy + width/2
        self.draw.ellipse([ptA1, ptA2, ptA3, ptA4], fill=color, outline=outline)
        logger.info(' circle drawn, %s ',[ptA1, ptA2, ptA3, ptA4, self.xScale, self.yScale])
        return self.img

    def __init__(self, width, height, myScale, minGeo, maxGeo, midGeo, xw650, yw450, myNight=True, myFakeImg=False, myImgStorage = './myImgStorage', mySec = 600):
        self.xScale=myScale[0]
        self.yScale=myScale[1]
        self.xStart=minGeo[0]
        self.yStart=minGeo[1]
        self.picWidth=width
        self.picHeight=height
        mapRequest='https://static-maps.yandex.ru/1.x/?ll='+str(midGeo[0])+','+str(midGeo[1])+'&z=15&l=map&size=650,450'
        logger.info('MAP REQUESTING: '+mapRequest)

        if not os.path.exists(myImgStorage):
            logger.info('no exists path')
            os.makedirs(myImgStorage)
        myCleanUrlText=str(re.sub('[^\w\-_\. ]', '_', mapRequest))
        myFileName = myImgStorage+'/myYandexImg_'+myCleanUrlText+'.jpg'
        try:
            logger.info('try1 '+str(time.time()))
            stats = os.stat(myFileName)
            myFileTime = stats.st_mtime
        except: # проверять, что за ошибка, не будем пока; - считаем, что нет файла..
            logger.info('except1 '+str(time.time()))
            myFileTime = time.time()-mySec-1 # обновление нужно сразу, файл отсутствует..
        weReadFile=False
        if((time.time()-myFileTime)>mySec):
            try:
                logger.info('try2 '+str(time.time()))
                response = requests.get(mapRequest) # здесь ещё, видимо, timeout чёто указать, чтоль...
                foreground = Image.open(BytesIO(response.content))
                myJpg=Image.new("RGB", (650, 450)) # делается для перевода формата из BytesIO в JPG
                myJpg.paste(foreground)
                myJpg = myJpg.save(myFileName)
            except:
                logger.info('except2 '+str(time.time()))
                weReadFile=True
        else:
            weReadFile=True
        if(weReadFile):
            try:
                logger.info('try3 '+str(time.time()))
                foreground = Image.open(myFileName)
            except:
                logger.info('except3 '+str(time.time()))
                foreground = Image.new("RGB", (int(width), int(height))) # здесь надо бы грузить картинку "ХОРОШЕГО ДНЯ!", чёнить.. ориентир по флагу myFakeImg, если jsOn не прогрузился, напр.

        if(myNight): # ночной режим
            foreground = ImageOps.invert(foreground.convert('RGB'))
        newSize = (int(width*xw650/(maxGeo[0]-minGeo[0])), int(height*yw450/(maxGeo[1]-minGeo[1]))) 
        foreground = foreground.resize(newSize, resample=Image.LANCZOS) # получили карту из яндекса в нужных нам пропорциях.. теперь ставим её по центру нашей картинки и подрезаем по её границам..
        offset = int((width-newSize[0])/2), int((height-newSize[1])/2)
        self.img=Image.new("RGB", (int(width), int(height)))
        self.img.paste(foreground, offset) 
        self.draw = ImageDraw.Draw(self.img)
        logger.info('............. !!! init of myImage class, width: %s, height: %s, myScale: %s, minGeo: %s, maxGeo: %s, midGeo: %s ', str(width), str(height), str(myScale), str(minGeo), str(maxGeo), str(midGeo))

def probkShowJson(request): # удалить потом, ненужная функция...
    jsOnCode='{test}'
    return HttpResponse(jsOnCode, content_type='application/json')

def probkShowHTML(request):

    def getJsOnCached(myUrl, mySec = 15, myJsOnStorage = './myJsOnStorage'):
        """ if more than mySec passed since last get of myUrl, tries to refresh data by getting it from myUrl (then stores to local file);
        otherwise, gets data from local file """
        myJsOnText='{}'
        if not os.path.exists(myJsOnStorage):
            os.makedirs(myJsOnStorage)
        myCleanUrlText=str(re.sub('[^\w\-_\. ]', '_', myUrl)) # для имени файла - очистка строки от дряни.. можно бы ещё подрезать (начало обрезать...)
        myFileName = myJsOnStorage+'/myJsOn_'+myCleanUrlText+'.txt'
        try:
            stats = os.stat(myFileName)
            myFileTime = stats.st_mtime
        except: # проверять, что за ошибка, не будем пока; - считаем, что нет файла..
            my_file = open(myFileName, "w+")
            my_file.write("{}")
            my_file.close()
            myFileTime = time.time()-mySec-1 # новый пустой файл требует обновления сразу..
        weReadFile=False
        if((time.time()-myFileTime)>mySec):
            try:
                response = requests.get(myUrl) # здесь ещё, видимо, timeout чёто указать, чтоль... 
                myJsOnText = response.text
                my_file = open(myFileName, "w+")
                my_file.write(str(myJsOnText))
                my_file.close()
            except:
                weReadFile=True
        else:
            weReadFile=True
        logger.info('weReadFile: %s, now: %s, myFileTime: %s, delta: %s', str(weReadFile), str(time.time()), str(myFileTime), (time.time()-myFileTime))
        if(weReadFile):
            try: # возможно, инициализация файлом ещё не прошла ни разу...
                my_file = open(myFileName, "r")
                myJsOnText = my_file.read()
                my_file.close()
            except: # случай, когда камера ещё не запустилась; надо бы здесь предусмотреть также вариант, когда камера выведена из строя.... время больше чем час напр. 
                myJsOnText = '{}'
        return myJsOnText

    def getMinMaxCoords(allNodes):
        """of [10,10], [20,50], [100,40] - returns [10,10],[100,50] boundaries"""
        if(allNodes):
            minX, minY = allNodes[0]
            maxX, maxY = allNodes[0]
            for node in allNodes:
                if(minY>node[1]):
                    minY=node[1]
                if(minX>node[0]):
                    minX=node[0]
                if(maxY<node[1]):
                    maxY=node[1]
                if(maxX<node[0]):
                    maxX=node[0]
            midX = (maxX + minX)/2
            midY = (maxY + minY)/2
            return [minX, minY], [maxX, maxY], [midX, midY]
        else:
            return [0,0], [0,0], [0,0]

    myTimeStart=time.time()
    mymess="timeStart : "+str(myTimeStart)

    logger.info(' =============== init of probkShowHTML! =============== ')

    # response = requests.get("https://mob-aks.com/graphFull.json")
    # myJsOn = json.loads(response.text)
    jsOnText = getJsOnCached("https://mob-aks.com/graphFull.json")
    myJsOn = json.loads(jsOnText)

    preResampleScale = 3.5 # от начального масштаба зависит уровень сглаживания (чем больше тут число, тем глаже, - но медленнее..)
    resampleMethod=Image.LANCZOS # от этого тоже зависит скорость/качество; здесь возможны - LANCZOS, BILINEAR.. BICUBIC, ещё что-то возможно... (LANCZOS видимо самый медленный...)
    imgWprt, imgHprt = myJsOn["image"]['width'], myJsOn["image"]['height']
    imgW, imgH = preResampleScale * imgWprt, preResampleScale * imgHprt # юзаем увеличенную карту, потом сожмём для anti-aliasing сглаживания..

    mymess+=" - timeSpent1 : "+str(time.time()-myTimeStart)

    allNodesGeo=[] # соберём все точки Geo-координат lng/lat, чтоб границы зоны очертить... (представлено с ошибкой вроде.. вида 55.7389525936213 = lat = Y, 37,61455801 = lng = X)
    allNodesOur=[] # а так же и точки в неясной системе координат, представленные как 4188783.732476062 (недо-UTM какаято... ну окэ..)
    
    myNodes=myJsOn["graph"]['nodes']
    myLinks=myJsOn["graph"]['links']
    myLoads=myJsOn["loads"]

    # ЗАМЕТКИ:
    # LAT - LATITUDE - ШИРОТА - угол между макушкой чоловека и плоскостью экватора (на экваторе = 0, вниз от экватора - отрицательное, вверх - положительное, до 90с градусов)
    # ДЛЯ НАС ШИРОТА ЭТО YY-координата, причём чем больше, тем ВЫШЕ точка. (т.е. инверт для стандартного Y.)
    
    # LNG - LONGITUDE - ДОЛГОТА, угол между гринвичевским меридианом и меридианом, проходящим через макушку человека; к востоку - положителен, до 180c градусов)
    # ДЛЯ НАС ДОЛГОТА ЭТО XX-координата, причём чем больше, тем ПРАВЕЕ точка. (стандарт для X.)

    # + на квадрате карты, XX будет вдвое меньше YY, т.е. гео-масштаб "сплющен" по Y: градусы от экватора до северного полюса - только 0-90, градусы от гринвича до контр-гринвича - 0-180.
    # поэтому координаты москвы 37х55...

    mymess+=" - timeSpent2 : "+str(time.time()-myTimeStart)

    if myNodes:
        for node in myNodes:
            allNodesGeo.append([node["location"]["lat"], node["location"]["lng"]])
            if(node["geometry"]["center"]):
                allNodesOur.append(node["geometry"]["center"])
    if myLinks:
        for link in myLinks:
            allNodesGeo.append([link["startPoint"]["lat"], link["startPoint"]["lng"]])
            allNodesGeo.append([link["endPoint"]["lat"], link["endPoint"]["lng"]])
            if(link["geometry"]['coordinates']):
                for coords in link["geometry"]['coordinates']:
                    allNodesOur.append(coords)

    mymess+=" - timeSpent3 : "+str(time.time()-myTimeStart)

    minGeo, maxGeo, midGeo = getMinMaxCoords(allNodesGeo)
    minOur, maxOur, midOur = getMinMaxCoords(allNodesOur)

    mymess+=" - timeSpent4 : "+str(time.time()-myTimeStart)

    # вычисляем коэффициенты сжатия для карты, исходя из min/max и размеров карты...
    scaleGeo=imgW/(maxGeo[0]-minGeo[0]), imgH/(maxGeo[1]-minGeo[1])
    scaleOur=imgW/(maxOur[0]-minOur[0]), imgH/(maxOur[1]-minOur[1])
    # теперь достаточно помножить (X-minX) или (Y-minY) точки на этот scale, 
    # чтоб получить её координаты на картинке...

    mymess+=" - timeSpent5 : "+str(time.time()-myTimeStart)

    myImageGeo = myImage(imgW, imgH, scaleGeo, minGeo, maxGeo, midGeo, 0.0277095, 0.0108775, random.choice([True, False]))
    myImageOur = myImage(imgW, imgH, scaleOur, minOur, maxOur, midGeo, 3074.6175307731514, 2158.172434062504, random.choice([True, False]))

    mymess+=" - timeSpent6 : "+str(time.time()-myTimeStart)

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
            myImageGeo.arrowedLine([link["startPoint"]["lat"], link["startPoint"]["lng"]], [link["endPoint"]["lat"], link["endPoint"]["lng"]], 0.00017, myColor)
            if(link["geometry"]['coordinates']):
                prevCoords=link["geometry"]['coordinates'][0]
                for coords in link["geometry"]['coordinates']:
                    if(coords==prevCoords):
                        pass # для одной линии-сплайна используются две или более точек; первая не участвует в построении...
                    else:
                        myImageOur.arrowedLine(prevCoords, coords, 26, myColor) # 26 как средняя расчётная эстетичная толщина..
                        prevCoords=coords

    mymess+=" - timeSpent7 : "+str(time.time()-myTimeStart)

    if(myNodes):
        for node in myNodes:
            myImageGeo.circle([node["location"]["lat"], node["location"]["lng"]], 0.000007*node["geometry"]["radius"], 'red') # с радиусом в случае гео-модели нет ясности.
            if(node["geometry"]["center"]):
                myImageOur.circle(node["geometry"]["center"], node["geometry"]["radius"], 'red')

    mymess+=" - timeSpent8 : "+str(time.time()-myTimeStart)

    myImageGeo.img = myImageGeo.img.resize((imgWprt, imgHprt), resample=resampleMethod)
    myImageOur.img = myImageOur.img.resize((imgWprt, imgHprt), resample=resampleMethod)

    mymess+=" - timeSpent9 : "+str(time.time()-myTimeStart)

    img_file_geo = BytesIO()
    myImageGeo.img.save(img_file_geo,format="PNG")
    img_file_our = BytesIO()
    myImageOur.img.save(img_file_our,format="PNG")

    mymess+=" - timeSpentTotal : "+str(time.time()-myTimeStart)

    context = {
        'img_str_geo': base64.b64encode(img_file_geo.getvalue()).decode('utf-8'),
        'img_str_our': base64.b64encode(img_file_our.getvalue()).decode('utf-8'),
        'mymess': mymess,
    }
    return render(request,
        'events/probks_template.html',
        context=context
    )

