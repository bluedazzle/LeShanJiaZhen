from HomeApi.models import *
from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import json
from HomeApi.errorType import *


@csrf_exempt
def add_homeitem_p(request):
    try:
        req = json.loads(request.body)
        item_name = req['item_name']
        if len(HomeItem_P.objects.filter(item_name=item_name)) != 0:
            raise AlreadyExitError
        p = HomeItem_P(item_name=item_name)
        p.save()
        status = 1
    except AlreadyExitError:
        status = 6
    except Exception:
        status = 2
    return HttpResponse(json.dumps({'status': status, 'body': 'null'}))


@csrf_exempt
def del_homeitem_p(request):
    try:
        req = json.loads(request.body)
        item_name = req['item_name']
        if len(HomeItem_P.objects.filter(item_name=item_name)) == 0:
            raise NoneExistError
        p = HomeItem_P.objects.get(item_name=item_name)
        p.delete()
        status = 1
    except NoneExistError:
        status = 7
    except Exception:
        status = 2
    return HttpResponse(json.dumps({'status': status, 'body': 'null'}))


@csrf_exempt
def change_homeitem_p(request):
    try:
        req = json.loads(request.body)
        item_name = req['item_name']
        new_item_name = req.get('new_item_name')
        if len(HomeItem_P.objects.filter(item_name=item_name)) == 0:
            raise NoneExistError
        HomeItem_P.objects.get(item_name=item_name).update(item_name=new_item_name)
        status = 1
    except NoneExistError:
        status = 7
    except Exception:
        status = 2
    return HttpResponse(json.dumps({'status': status, 'body': 'null'}))


@csrf_exempt
def add_homeitem_o(request):
    try:
        req = json.loads(request.body)
        item_name = req['item_name']
        parent_item = req['parent_item']
        if len(HomeItem_O.objects.filter(item_name=item_name)) != 0:
            raise AlreadyExitError
        if len(HomeItem_P.objects.filter(item_name=parent_item)) == 0:
            raise NoneExistError
        p = HomeItem_O(item_name=item_name)
        p_parent = HomeItem_P.objects.get(item_name=parent_item)
        p.parent_item = p_parent
        p.save()
        status = 1
    except AlreadyExitError:
        status = 6
    except NoneExistError:
        status = 7
    except Exception:
        status = 2
    return HttpResponse(json.dumps({'status': status, 'body': 'null'}))


@csrf_exempt
def del_homeitem_o(request):
    try:
        req = json.loads(request.body)
        item_name = req['item_name']
        if len(HomeItem_O.objects.filter(item_name=item_name)) == 0:
            raise NoneExistError
        p = HomeItem_O.objects.get(item_name=item_name)
        p.delete()
        status = 1
    except NoneExistError:
        status = 7
    except Exception:
        status = 2
    return HttpResponse(json.dumps({'status': status, 'body': 'null'}))


@csrf_exempt
def change_homeitem_o(request):
    try:
        req = json.loads(request.body)
        item_name = req['item_name']
        new_item_name = req['new_item_name']
        parent_item = req['parent_item']
        if len(HomeItem_O.objects.filter(item_name=item_name)) == 0:
            raise NoneExistError
        if len(HomeItem_P.objects.filter(item_name=parent_item)) == 0:
            raise NoneExistError
        p_parent = HomeItem_P.objects.get(item_name=parent_item)
        HomeItem_O.objects.filter(item_name=item_name).update(item_name=new_item_name, parent_item=p_parent)
        status = 1
    except NoneExistError:
        status = 7
    except Exception:
        status = 2
    return HttpResponse(json.dumps({'status': status, 'body': 'null'}))


@csrf_exempt
def add_homeitem(request):
    try:
        req = json.loads(request.body)
        title = req['title']
        content = req['content']
        parent_item = req['parent_item']
        if len(HomeItem.objects.filter(title=title)) != 0:
            raise AlreadyExitError
        if len(HomeItem_O.objects.filter(item_name=parent_item)) == 0:
            raise NoneExistError
        p_parent = HomeItem_O.objects.get(item_name=parent_item)
        p = HomeItem(title=title, content=content)
        p.parent_item = p_parent
        p.save()
        status = 1
    except AlreadyExitError:
        status = 6
    except NoneExistError:
        status = 7
    except Exception:
        status = 2
    return HttpResponse(json.dumps({'status': status, 'body': 'null'}))


@csrf_exempt
def del_homeitem(request):
    try:
        req = json.loads(request.body)
        title = req['title']
        if len(HomeItem.objects.filter(title=title)) == 0:
            raise NoneExistError
        p = HomeItem.objects.get(title=title)
        p.delete()
        status = 1
    except NoneExistError:
        status = 7
    except Exception:
        status = 2
    return HttpResponse(json.dumps({'status': status, 'body': 'null'}))


@csrf_exempt
def change_homeitem(request):
    try:
        req = json.loads(request.body)
        title = req['title']
        new_title = req['new_title']
        content = req['content']
        parent_item = req['parent_item']
        if len(HomeItem.objects.filter(title=title)) == 0:
            raise NoneExistError
        if len(HomeItem_O.objects.filter(item_name=parent_item)) == 0:
            raise NoneExistError
        p_parent = HomeItem_O.objects.get(item_name=parent_item)
        HomeItem.objects.filter(title=title).update(title=new_title, content=content, parent_item=p_parent)
        status = 1
    except NoneExistError:
        status = 7
    except Exception:
        status = 2
    return HttpResponse(json.dumps({'status': status, 'body': 'null'}))


@csrf_exempt
def add_block(request):
    try:
        req = json.loads(request.body)
        area_name = req['area_name']
        area_tel = int(req['area_tel'])
        area_info = req['area_info']
        area_admin = req['area_admin']
        if len(Block.objects.filter(area_name=area_name)) != 0:
            raise AlreadyExitError
        if len(HomeAdmin.objects.filter(username=area_admin)) == 0:
            raise NoneExistError
        p = Block(area_name=area_name, area_tel=area_tel, area_info=area_info)
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
    return HttpResponse(json.dumps({"status": status, "body": 'null'}))



@csrf_exempt
def del_block(request):
    try:
        req = json.loads(request.body)
        area_name = req['area_name']
        if len(Block.objects.filter(area_name=area_name)) == 0:
            raise NoneExistError
        p = Block.objects.get(area_name=area_name)
        p.delete()
        status = 1
    except NoneExistError:
        status = 7
    except Exception:
        status = 2
    return HttpResponse(json.dumps({"status": status, "body": 'null'}))


@csrf_exempt
def change_block(request):
    try:
        req = json.loads(request.body)
        area_name = req['area_name']
        new_area_name = req['new_area_name']
        area_tel = int(req['area_tel'])
        area_info = req['area_info']
        area_admin = req['area_admin']
        if len(Block.objects.filter(area_name=area_name)) == 0:
            raise NoneExistError
        if len(HomeAdmin.objects.filter(username=area_admin)) == 0:
            raise NoneExistError
        p = Block.objects.get(area_name=area_name)
        p.area_name = new_area_name
        p.area_tel = area_tel
        p.area_info = area_info
        p_admin = HomeAdmin.objects.get(username=area_admin)
        p.area_admin = p_admin
        p.save()
        status = 1
    except NoneExistError:
        status = 7
    except Exception:
        status = 2
    return HttpResponse(json.dumps({"status": status, "body": 'null'}))


