#!/usr/bin/env python3
# \myclub_root\myProbkaGen.py
# скрипт создаёт произвольный ориентированный граф в JSON.. ПОКА НЕ РАБОТАЕТ!!
# с к-вом узлов произвольным 1 до N, 
# к-вом линков произвольным до полного ориентированного графа.... каковое n*(n-1) рёбер.

import json
import itertools
import networkx as nx
import numpy.random as rnd
import matplotlib.pyplot as plt

graph=nx.Graph()
graph.add_node('A')
graph.add_node('B')
graph.add_node('C')

def add_double_edge(src,dst,graph=None):
    graph.add_edge(src,dst)
    graph.add_edge(dst,src)

add_double_edge('A','B',graph=graph)
add_double_edge('A','C',graph=graph)

print('graph here: '+str(graph.nodes()))

nx.draw_circular(graph,
    node_color='red',
    node_size=1000,
    with_labels=True
)


'''
{
	"graph": { 
	    "nodes": [
              {
                "location": { - координаты узла
                  "lng": 55.7389525936213,
                  "lat": 37.6284844875446
                },
                "geometry": { - геометрия, используется для отображения на карте
                  "type": "Circle",
                  "center": [
                    4188783.732476062,
                    7506623.048889009
                  ],
                  "radius": 120.10278760269284
                },
                "id": 66, - id
                "controllerId": null - сейчас не используется
              },
	    ], - массив узлов графа
	    "links": [
	        {
                "geometry": { - геометрия в метрах
                  "type": "LineString",
                  "coordinates": [
                    [
                      4188790.592865324,
                      7506722.035869018
                    ],
                    [
                      4188777.7608368318,
                      7507456.093065263
                    ],
                    [
                      4188583.6824447014,
                      7507927.852849211
                    ]
                  ]
                },
                "startPoint": { - начало линка, градусы 
                  "lng": 55.7394531868025,
                  "lat": 37.6285461154699
                },
                "endPoint": { - конец линка, градусы
                  "lng": 55.7455506829566,
                  "lat": 37.626687407537
                },
                "length": 1244, - длина, метры
                "id": 136, - id
                "fromNodeId": 66, - из какого узла
                "toNodeId": 68 - в какой узел
            },
	    ] - массив линков (связей) графа
	}, - граф дорог
	"loads": [
	    {
	        "link_id": 45, - id линка
	        "load": 10 - баллы, 0-10
	    }
	], - массив балльности линков
	"image": {
	    "width": 200, - требуемая ширина изображения, пиксели
	    "height": 300, - требуемая высота изображения, пиксели
	}
}


'''