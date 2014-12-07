from HomeApi.models import *
from HomeApi.errorType import *


def add_block(area_id, area_name, area_tel, area_info, area_admin, lat, lng):
    try:
        if len(Block.objects.filter(area_name=area_name)) != 0:
            raise AlreadyExitError
        if len(HomeAdmin.objects.filter(username=area_admin)) == 0:
            raise NoneExistError
        p = Block(area_id=area_id, area_name=area_name, area_tel=area_tel, area_info=area_info, lat=lat, lng=lng)
        p_admin = HomeAdmin.objects.get(username=area_admin)
        p.area_admin = p_admin
        p.save()
        status = 1
    except AlreadyExitError:
        status = 6
    except NoneExistError:
        status = 7
    except Exception:
        status = 2
    return status


def del_block(area_name):
    try:
        if len(Block.objects.filter(area_name=area_name)) == 0:
            raise NoneExistError
        p = Block.objects.get(area_name=area_name)
        p.delete()
        status = 1
    except NoneExistError:
        status = 7
    except Exception:
        status = 2
    return status


def change_block(area_id, area_name, new_area_name, area_tel, area_info, area_admin, lat, lng):
    try:
        if len(Block.objects.filter(area_name=area_name)) == 0:
            raise NoneExistError
        if len(Block.objects.filter(area_name=new_area_name)) != 0:
            raise AlreadyExitError
        if len(HomeAdmin.objects.filter(username=area_admin)) == 0:
            raise NoneExistError
        p = Block.objects.get(area_name=area_name)
        p.area_id = area_id
        p.area_name = new_area_name
        p.area_tel = area_tel
        p.area_info = area_info
        p_admin = HomeAdmin.objects.get(username=area_admin)
        p.area_admin = p_admin
        p.lat = lat
        p.lng = lng
        p.save()
        status = 1
    except NoneExistError:
        status = 7
    except AlreadyExitError:
        status = 6
    except Exception:
        status = 2
    return status
