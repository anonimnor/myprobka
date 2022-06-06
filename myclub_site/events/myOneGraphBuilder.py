# \myclub_root\events\myprobksCheck.py
# скрипт пока отображает хоть чегото.
from django.shortcuts import render
from django.http import HttpResponse
from django.dispatch import receiver
from django.db.models.signals import post_save
import math, random

def showHTML(request):
    # mymess = "{test}"+str(request)

    '''{
	"graph": { 
	    "nodes": [
              {
                "location": {
                  "lng": 55.7389525936213,
                  "lat": 37.6284844875446
                },
                "geometry": {
                  "type": "Circle",
                  "center": [
                    4188783.732476062,
                    7506623.048889009
                  ],
                  "radius": 120.10278760269284
                },
                "id": 66,
                "controllerId": null
              },
              {
                "location": {
                  "lng": 55.7391337917495,
                  "lat": 37.6244611740223
                },
                "geometry": {
                  "type": "Circle",
                  "center": [
                    4188335.8592634536,
                    7506658.878746019
                  ],
                  "radius": 118.42085441760719
                },
                "id": 67,
                "controllerId": null
              },
              {
                "location": {
                  "lng": 55.7459130170976,
                  "lat": 37.6265801191441
                },
                "geometry": {
                  "type": "Circle",
                  "center": [
                    4188571.7391554276,
                    7507999.512562427
                  ],
                  "radius": 91.00634779781103
                },
                "id": 68,
                "controllerId": 11371
              },
              {
                "location": {
                  "lng": 55.7456714613748,
                  "lat": 37.6244611740223
                },
                "geometry": {
                  "type": "Circle",
                  "center": [
                    4188335.8592634536,
                    7507951.739419748
                  ],
                  "radius": 95.59292743168771
                },
                "id": 69,
                "controllerId": 11189
              },
              {
                "location": {
                  "lng": 55.7445089535424,
                  "lat": 37.6347608566395
                },
                "geometry": {
                  "type": "Circle",
                  "center": [
                    4189482.4146877313,
                    7507721.831170609
                  ],
                  "radius": 63.47943407576531
                },
                "id": 70,
                "controllerId": 11250
              },
              {
                "location": {
                  "lng": 55.7478439346858,
                  "lat": 37.625723090474
                },
                "geometry": {
                  "type": "Circle",
                  "center": [
                    4188476.3351602764,
                    7508381.406100554
                  ],
                  "radius": 50.06261869892478
                },
                "id": 71,
                "controllerId": null
              },
              {
                "location": {
                  "lng": 55.7484666578163,
                  "lat": 37.6245563295525
                },
                "geometry": {
                  "type": "Circle",
                  "center": [
                    4188346.4519286198,
                    7508504.571234021
                  ],
                  "radius": 65.45864445203915
                },
                "id": 72,
                "controllerId": 12987
              },
              {
                "location": {
                  "lng": 55.7423952142014,
                  "lat": 37.615770816814
                },
                "geometry": {
                  "type": "Circle",
                  "center": [
                    4187368.4531242196,
                    7507303.816172174
                  ],
                  "radius": 97.48604046693072
                },
                "id": 73,
                "controllerId": 11339
              }
            ],
	    "links": [
              {
                "geometry": {
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
                "startPoint": {
                  "lng": 55.7394531868025,
                  "lat": 37.6285461154699
                },
                "endPoint": {
                  "lng": 55.7455506829566,
                  "lat": 37.626687407537
                },
                "length": 1244,
                "id": 136,
                "fromNodeId": 66,
                "toNodeId": 68
              },
              {
                "geometry": {
                  "type": "LineString",
                  "coordinates": [
                    [
                      4188344.8167416328,
                      7507886.051351768
                    ],
                    [
                      4188410.504812815,
                      7507256.043032699
                    ],
                    [
                      4188350.7883844674,
                      7506739.49592749
                    ]
                  ]
                },
                "startPoint": {
                  "lng": 55.7453393198302,
                  "lat": 37.6245416404178
                },
                "endPoint": {
                  "lng": 55.7395414844783,
                  "lat": 37.6245952845981
                },
                "length": 1153,
                "id": 137,
                "fromNodeId": 69,
                "toNodeId": 67
              },
              {
                "geometry": {
                  "type": "LineString",
                  "coordinates": [
                    [
                      4188646.9771861513,
                      7507998.322889239
                    ],
                    [
                      4188938.094774347,
                      7507958.014300104
                    ],
                    [
                      4189162.031380651,
                      7507886.354586086
                    ],
                    [
                      4189382.982165538,
                      7507799.765764982
                    ],
                    [
                      4189445.684415303,
                      7507743.035158052
                    ]
                  ]
                },
                "startPoint": {
                  "lng": 55.7459070017617,
                  "lat": 37.6272559938735
                },
                "endPoint": {
                  "lng": 55.7446161708123,
                  "lat": 37.6344309029884
                },
                "length": 851,
                "id": 138,
                "fromNodeId": 68,
                "toNodeId": 70
              },
              {
                "geometry": {
                  "type": "LineString",
                  "coordinates": [
                    [
                      4188538.8951140977,
                      7508056.243164417
                    ],
                    [
                      4188473.2070429153,
                      7508369.754413243
                    ]
                  ]
                },
                "startPoint": {
                  "lng": 55.7461998625512,
                  "lat": 37.6262850761009
                },
                "endPoint": {
                  "lng": 55.7477850232197,
                  "lat": 37.6256949901176
                },
                "length": 320,
                "id": 139,
                "fromNodeId": 68,
                "toNodeId": 71
              },
              {
                "geometry": {
                  "type": "LineString",
                  "coordinates": [
                    [
                      4188342.4234011555,
                      7508465.603937479
                    ],
                    [
                      4188369.2957939124,
                      7508001.308707075
                    ]
                  ]
                },
                "startPoint": {
                  "lng": 55.7482696401716,
                  "lat": 37.6245201406745
                },
                "endPoint": {
                  "lng": 55.745922098929,
                  "lat": 37.6247615394859
                },
                "length": 465,
                "id": 140,
                "fromNodeId": 72,
                "toNodeId": 69
              },
              {
                "geometry": {
                  "type": "LineString",
                  "coordinates": [
                    [
                      4188288.086135192,
                      7507957.711063071
                    ],
                    [
                      4187953.6741364445,
                      7507790.505063698
                    ],
                    [
                      4187598.3613877753,
                      7507512.82367188
                    ],
                    [
                      4187413.240459897,
                      7507345.617672507
                    ]
                  ]
                },
                "startPoint": {
                  "lng": 55.7457016559244,
                  "lat": 37.6240320207094
                },
                "endPoint": {
                  "lng": 55.7426065932905,
                  "lat": 37.6161731482958
                },
                "length": 1074,
                "id": 141,
                "fromNodeId": 69,
                "toNodeId": 73
              },
              {
                "geometry": {
                  "type": "LineString",
                  "coordinates": [
                    [
                      4188416.766858398,
                      7507968.692104975
                    ],
                    [
                      4188494.7714429274,
                      7507986.233805802
                    ]
                  ]
                },
                "startPoint": {
                  "lng": 55.7457571795437,
                  "lat": 37.6251879793137
                },
                "endPoint": {
                  "lng": 55.7458458757645,
                  "lat": 37.6258887064188
                },
                "length": 80,
                "id": 142,
                "fromNodeId": 69,
                "toNodeId": 68
              },
              {
                "geometry": {
                  "type": "LineString",
                  "coordinates": [
                    [
                      4188493.5392076266,
                      7508026.207072815
                    ],
                    [
                      4188401.3519713646,
                      7508004.3732537
                    ]
                  ]
                },
                "startPoint": {
                  "lng": 55.7460479921124,
                  "lat": 37.6258776370608
                },
                "endPoint": {
                  "lng": 55.7459375941659,
                  "lat": 37.6250495050274
                },
                "length": 95,
                "id": 143,
                "fromNodeId": 68,
                "toNodeId": 69
              }
            ]
	}, 
	"loads": [
	    {
	        "link_id": 141,
	        "load": 3
	    },
	    {
	        "link_id": 143,
	        "load": 10
	    },
	    {
	        "link_id": 142,
	        "load": 5
	    },
	    {
	        "link_id": 139,
	        "load": 1
	    },
	    {
	        "link_id": 138,
	        "load": 2
	    }
	], 
	"image": {
	    "width": 200,
	    "height": 300,
	    "format": "svg"
	}
    }'''
    if(random.randint(0,2)==1):
        mymess='{"graph":{"nodes":[{"location":{"lng":55.7389525936213,"lat":37.6284844875446},"geometry":{"type":"Circle","center":[4188783.732476062,7506623.048889009],"radius":120.10278760269284},"id":66,"controllerId":null}],"links":[{"geometry":{"type":"LineString","coordinates":[[4188790.592865324,7506722.035869018],[4188777.7608368318,7507456.093065263],[4188583.6824447014,7507927.852849211]]},"startPoint":{"lng":55.7394531868025,"lat":37.6285461154699},"endPoint":{"lng":55.7455506829566,"lat":37.626687407537},"length":1244,"id":136,"fromNodeId":66,"toNodeId":68}]},"loads":[{"link_id":45,"load":10}],"image":{"width":'+str(random.randint(0,500))+',"height":'+str(random.randint(0,500))+'}}'
    else:
        mymess='{"graph":{"nodes":[{"location":{"lng":55.7389525936213,"lat":37.6284844875446},"geometry":{"type":"Circle","center":[4188783.732476062,7506623.048889009],"radius":120.10278760269284},"id":66,"controllerId":null},{"location":{"lng":55.7391337917495,"lat":37.6244611740223},"geometry":{"type":"Circle","center":[4188335.8592634536,7506658.878746019],"radius":118.42085441760719},"id":67,"controllerId":null},{"location":{"lng":55.7459130170976,"lat":37.6265801191441},"geometry":{"type":"Circle","center":[4188571.7391554276,7507999.512562427],"radius":91.00634779781103},"id":68,"controllerId":11371},{"location":{"lng":55.7456714613748,"lat":37.6244611740223},"geometry":{"type":"Circle","center":[4188335.8592634536,7507951.739419748],"radius":95.59292743168771},"id":69,"controllerId":11189},{"location":{"lng":55.7445089535424,"lat":37.6347608566395},"geometry":{"type":"Circle","center":[4189482.4146877313,7507721.831170609],"radius":63.47943407576531},"id":70,"controllerId":11250},{"location":{"lng":55.7478439346858,"lat":37.625723090474},"geometry":{"type":"Circle","center":[4188476.3351602764,7508381.406100554],"radius":50.06261869892478},"id":71,"controllerId":null},{"location":{"lng":55.7484666578163,"lat":37.6245563295525},"geometry":{"type":"Circle","center":[4188346.4519286198,7508504.571234021],"radius":65.45864445203915},"id":72,"controllerId":12987},{"location":{"lng":55.7423952142014,"lat":37.615770816814},"geometry":{"type":"Circle","center":[4187368.4531242196,7507303.816172174],"radius":97.48604046693072},"id":73,"controllerId":11339}],"links":[{"geometry":{"type":"LineString","coordinates":[[4188790.592865324,7506722.035869018],[4188777.7608368318,7507456.093065263],[4188583.6824447014,7507927.852849211]]},"startPoint":{"lng":55.7394531868025,"lat":37.6285461154699},"endPoint":{"lng":55.7455506829566,"lat":37.626687407537},"length":1244,"id":136,"fromNodeId":66,"toNodeId":68},{"geometry":{"type":"LineString","coordinates":[[4188344.8167416328,7507886.051351768],[4188410.504812815,7507256.043032699],[4188350.7883844674,7506739.49592749]]},"startPoint":{"lng":55.7453393198302,"lat":37.6245416404178},"endPoint":{"lng":55.7395414844783,"lat":37.6245952845981},"length":1153,"id":137,"fromNodeId":69,"toNodeId":67},{"geometry":{"type":"LineString","coordinates":[[4188646.9771861513,7507998.322889239],[4188938.094774347,7507958.014300104],[4189162.031380651,7507886.354586086],[4189382.982165538,7507799.765764982],[4189445.684415303,7507743.035158052]]},"startPoint":{"lng":55.7459070017617,"lat":37.6272559938735},"endPoint":{"lng":55.7446161708123,"lat":37.6344309029884},"length":851,"id":138,"fromNodeId":68,"toNodeId":70},{"geometry":{"type":"LineString","coordinates":[[4188538.8951140977,7508056.243164417],[4188473.2070429153,7508369.754413243]]},"startPoint":{"lng":55.7461998625512,"lat":37.6262850761009},"endPoint":{"lng":55.7477850232197,"lat":37.6256949901176},"length":320,"id":139,"fromNodeId":68,"toNodeId":71},{"geometry":{"type":"LineString","coordinates":[[4188342.4234011555,7508465.603937479],[4188369.2957939124,7508001.308707075]]},"startPoint":{"lng":55.7482696401716,"lat":37.6245201406745},"endPoint":{"lng":55.745922098929,"lat":37.6247615394859},"length":465,"id":140,"fromNodeId":72,"toNodeId":69},{"geometry":{"type":"LineString","coordinates":[[4188288.086135192,7507957.711063071],[4187953.6741364445,7507790.505063698],[4187598.3613877753,7507512.82367188],[4187413.240459897,7507345.617672507]]},"startPoint":{"lng":55.7457016559244,"lat":37.6240320207094},"endPoint":{"lng":55.7426065932905,"lat":37.6161731482958},"length":1074,"id":141,"fromNodeId":69,"toNodeId":73},{"geometry":{"type":"LineString","coordinates":[[4188416.766858398,7507968.692104975],[4188494.7714429274,7507986.233805802]]},"startPoint":{"lng":55.7457571795437,"lat":37.6251879793137},"endPoint":{"lng":55.7458458757645,"lat":37.6258887064188},"length":80,"id":142,"fromNodeId":69,"toNodeId":68},{"geometry":{"type":"LineString","coordinates":[[4188493.5392076266,7508026.207072815],[4188401.3519713646,7508004.3732537]]},"startPoint":{"lng":55.7460479921124,"lat":37.6258776370608},"endPoint":{"lng":55.7459375941659,"lat":37.6250495050274},"length":95,"id":143,"fromNodeId":68,"toNodeId":69}]},"loads":[{"link_id":141,"load":3},{"link_id":143,"load":10},{"link_id":142,"load":5},{"link_id":139,"load":1},{"link_id":138,"load":2}],"image":{"width":'+str(random.randint(0,500))+',"height":'+str(random.randint(0,500))+',"format":"svg"}}'
    context = {
        'mymess': mymess,
    }
    return render(request,
        'events/oneGraph.html',
        context=context
    )
