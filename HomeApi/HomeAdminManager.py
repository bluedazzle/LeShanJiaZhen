# -*- coding:utf8 -*-
from HomeApi.models import *
from HomeApi.errorType import *
from HomeApi.location_process import *


def add_block(area_id, area_name, area_tel, area_info, area_admin, area_address):
    try:
        #判断该地区id和管理员是否存在
        if len(Block.objects.filter(area_id=area_id)) != 0:
            raise AlreadyExitError
        # if len(HomeAdmin.objects.filter(username=area_admin)) == 0:
        #     raise NoneExistError
        #从百度云获得该地址的经纬度
        location = BaiduAddress2Location(area_address)
        lat = float(location['lat'])
        lng = float(location['lng'])
        #将地区信息同步到百度自定义地图
        r_status = addBlockOnBaidu(name=area_name, address=area_address, latitude=lat, longitude=lng)
        if r_status['status'] == 2:
            raise Exception
        #将数据存入数据库
        p = Block(area_id=area_id, baidu_id=r_status['baidu_id'], area_name=area_name, area_tel=area_tel, area_info=area_info, area_address=area_address, lat=lat, lng=lng)
        # p_admin = HomeAdmin.objects.get(username=area_admin)
        # p.area_admin = p_admin
        p.save()
        status = 1
    except AlreadyExitError:
        status = 6
    except NoneExistError:
        status = 7
    except Exception:
        status = 2
    return status



def del_block(area_id):
    try:
        #判断该地区是否存在
        if len(Block.objects.filter(area_id=area_id)) == 0:
            raise NoneExistError
        p = Block.objects.get(area_id=area_id)
        #删除百度自定义地图上的服务点
        r_status = delBlockOnBaidu(baidu_id=p.baidu_id)
        if r_status == 2:
            raise Exception
        #更新数据库
        p.delete()
        status = 1
    except NoneExistError:
        status = 7
    except Exception:
        status = 2
    return status


def change_block(area_id, area_name, area_tel, area_info, area_admin, area_address):
    try:
        #判断该地区id和地区管理员是否存在
        if len(Block.objects.filter(area_id=area_id)) == 0:
            raise NoneExistError
        # if len(HomeAdmin.objects.filter(username=area_admin)) == 0:
        #     raise NoneExistError
        #从百度云获得该地址的经纬度
        location = BaiduAddress2Location(area_address)
        lat = float(location['lat'])
        lng = float(location['lng'])
        #将数据更新到百度自定义地图
        p = Block.objects.get(area_id=area_id)
        r_status = changeBlockOnBaidu(name=area_name, baidu_id=p.baidu_id, address=area_address, latitude=lat, longitude=lng)
        if r_status == 2:
            raise Exception
        #将数据更新到数据库
        p.area_name = area_name
        p.area_tel = area_tel
        p.area_info = area_info
        p.area_address = area_address
        # p_admin = HomeAdmin.objects.get(username=area_admin)
        # p.area_admin = p_admin
        p.lat = lat
        p.lng = lng
        p.save()
        status = 1
    except NoneExistError:
        status = 7
    except Exception:
        status = 2
    return status
