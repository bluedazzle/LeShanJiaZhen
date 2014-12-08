# -*- coding:utf8 -*-

# from HomeApi.models import *
#from math import *
import requests
import json


# def get_nearest(lat, lng):
#     blocks = Block.objects.all()
#     block_list = []
#     for block in blocks:
#         if block.lat and block.lng:
#             c = sin(lat)*sin(block.lat)*cos(lng-block.lng) + cos(lat)*cos(block.lat)
#             distance = acos(c)*3.14159/180
#             block_list.append((block.area_name, distance))
#     nearest_point = min(block_list, key=lambda x: x[1])
#     return nearest_point[0]


def BaiduLocation2Address(latitude, longitude):
    url = r'http://api.map.baidu.com/geocoder/v2/'
    ak = r'379b7404f384fa2c66a205200d6d291e'
    location = str(latitude)+','+str(longitude)
    payload = {'ak': ak, 'location': location, 'output': 'json'}
    r = requests.get(url, params=payload)
    return r.content


def BaiduAddress2Location(address):
    ak = r'379b7404f384fa2c66a205200d6d291e'
    url = r'http://api.map.baidu.com/geocoder/v2/'
    payload = {'ak': ak, 'address': address, 'output': 'json'}
    r = requests.get(url, params=payload)
    return json.loads(r.content)['result']['location']
s = BaiduAddress2Location('四川省成都市高新西区西源大道2006号')
print s


def addBlockOnBaidu(name, address, latitude, longitude):
    try:
        url = r'http://api.map.baidu.com/geodata/v3/poi/create'
        ak = '379b7404f384fa2c66a205200d6d291e'
        geotable_id = 87377
        coord_type = 1
        payload = {'ak': ak, 'title': name, 'address': address, 'latitude': latitude,
                   'longitude': longitude, 'geotable_id': geotable_id,
                   'coord_type': coord_type
        }
        r = requests.post(url, data=payload)
        if json.loads(r.content)['status'] != 0:
            raise Exception
        status = {'status': 1, 'baidu_id': json.loads(r.content)['id']}
    except Exception:
        status = {'status': 2, 'baidu_id': None}
    return status


def delBlockOnBaidu(baidu_id):
    try:
        url = r'http://api.map.baidu.com/geodata/v3/poi/delete'
        ak = '379b7404f384fa2c66a205200d6d291e'
        geotable_id = 87377
        payload = {'ak': ak, 'geotable_id': geotable_id, 'id': baidu_id}
        r = requests.post(url, data=payload)
        if json.loads(r.content)['status'] != 0:
            raise Exception
        status = 1
    except Exception:
        status = 2
    return status



def changeBlockOnBaidu(name, baidu_id, address, latitude, longitude):
    try:
        url = r'http://api.map.baidu.com/geodata/v3/poi/update'
        ak = '379b7404f384fa2c66a205200d6d291e'
        geotable_id = 87377
        coord_type = 1
        payload = {'ak': ak, 'title': name, 'address': address, 'latitude': latitude,
                   'longitude': longitude, 'geotable_id': geotable_id,
                   'coord_type': coord_type, 'id': baidu_id
        }
        r = requests.post(url, data=payload)
        if json.loads(r.content)['status'] != 0:
            raise Exception
        status = 1
    except Exception:
        status = 2
    return status


def getTheNearestFromBaidu(longitude, latitude):
    try:
        url = r'http://api.map.baidu.com/geosearch/v3/nearby'
        ak = '379b7404f384fa2c66a205200d6d291e'
        geotable_id = '87377'
        location = str(longitude)+','+str(latitude)
        radius = '10000000'
        sortby = 'distance:1'
        payload = {'ak': ak, 'geotable_id': geotable_id, 'location': location,
                   'radius': radius, 'sortby': sortby, 'q': None
        }
        r = json.loads(requests.get(url, params=payload).content)
        if r['status'] != 0:
            raise Exception
        nearest_id = r['contents'][0]['uid']
    except Exception:
        return {'status': 2, 'body': None}
    return {'status': 1, 'baidu_id': nearest_id}




