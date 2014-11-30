# -*- coding:utf8 -*-
from HomeApi.models import *
from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import json


@csrf_exempt
def add_homeitem_p(request):
    try:
        req = json.loads(request.raw_post_data)
        item_name = req.get('item_name')
        p = HomeItem_P(item_name=item_name)
        p.save()
        status = 1
    except Exception:
        status = 0
    return HttpResponse(json.dumps({'status': status}))


@csrf_exempt
def del_homeitem_p(request):
    try:
        req = json.loads(request.raw_post_data)
        item_name = req.get('item_name')
        p = HomeItem_P.objects.get(item_name)
        p.delete()
        status = 1
    except Exception:
        status = 0
    return HttpResponse(json.dumps({'status': status}))


@csrf_exempt
def add_homeitem_0(request):
    try:
        req = json.loads(request.raw_post_data)
        item_name = req.get('item_name')
        parent_item = req.get('parent_item')
        p = HomeItem_P(item_name=item_name, parent_item=parent_item)
        p.save()
        status = 1
    except Exception:
        status = 0
    return HttpResponse(json.dumps({'status': status}))


@csrf_exempt
def del_homeitem_0(request):
    try:
        req = json.loads(request.raw_post_data)
        item_name = req.get('item_name')
        p = HomeItem_O.objects.get(item_name)
        p.delete()
        status = 1
    except Exception:
        status = 0
    return HttpResponse(json.dumps({'status': status}))


@csrf_exempt
def add_homeitem(request):
    try:
        req = json.loads(request.raw_post_data)
        title = req.get('title')
        content = req.get('content')
        parent_item = req.get('parent_item')
        p = HomeItem_P(title=title, content=content, parent_item=parent_item)
        p.save()
        status = 1
    except Exception:
        status = 0
    return HttpResponse(json.dumps({'status': status}))


@csrf_exempt
def del_homeitem(request):
    try:
        req = json.loads(request.raw_post_data)
        title = req.get('title')
        p = HomeItem_O.objects.get(title)
        p.delete()
        status = 1
    except Exception:
        status = 0
    return HttpResponse(json.dumps({'status': status}))


@csrf_exempt
def change_homeitem(request):
    try:
        req = json.loads(request.raw_post_data)
        title = req.get('title')
        content = req.get('content')
        parent_item = req.get('parent_item')
        HomeItem_P.objects.filter(title=title).update(title=title, content=content, parent_item=parent_item)
        status = 1
    except Exception:
        status = 0
    return HttpResponse(json.dumps({'status': status}))