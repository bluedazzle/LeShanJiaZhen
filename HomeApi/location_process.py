# -*- coding:utf8 -*-
from HomeApi.models import *
import urllib2
import urllib
from math import *


def get_nearest(lat, lng):
    blocks = Block.objects.all()
    block_list = []
    for block in blocks:
        if block.lat and block.lng:
            c = sin(lat)*sin(block.lat)*cos(lng-block.lng) + cos(lat)*cos(block.lat)
            distance = acos(c)*3.14159/180
            block_list.append((block.area_name, distance))
    nearest_point = min(block_list, key=lambda x: x[1])
    return nearest_point[0]


def location2address(lat, lng):
    pass


def address2location(address):
    ak = r'379b7404f384fa2c66a205200d6d291e'
    url = r'http://api.map.baidu.com/geocoder/v2/'
    payload = {'ak': ak, 'address': address, 'output': 'json'}
    r = urllib2.urlopen(url, urllib.urlencode(payload))
    return r.read()

