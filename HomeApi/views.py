from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import json
from HomeApi.errorType import *
from HomeApi.models import *
import time
from PIL import Image
from HomeApi.HomeAdminManager import *
from HomeApi.location_process import *


@csrf_exempt
def pull_block_tel(request):
    if request.method == 'GET':
        try:
            area_id = request.GET['area_id']
            if len(Block.objects.filter(area_id=area_id)) == 0:
                raise NoneExistError
            tel = Block.objects.get(area_id=area_id).area_tel
            status = 1
        except NoneExistError:
            status = 7
            return HttpResponse(json.dumps({'status': status, 'body': None}))
        except Exception:
            status = 2
            return HttpResponse(json.dumps({'status': status, 'body': None}))
        return HttpResponse(json.dumps({'status': status, 'body': {'area_id': area_id, 'tel': tel}}))


@csrf_exempt
def make_appointment(request):
    if request.method == 'POST':
        try:
            req = request.POST
            pic = request.FILES.get('file')
            content = req['content']
            name = req['name']
            area_id = req['area_id']
            address = req['address']
            consumer = int(req['consumer'])
            if len(Consumer.objects.filter(phone=consumer)) == 0:
                status = 13
                return HttpResponse(json.dumps({'status': status, 'body': None}))
            else:
                if len(Block.objects.filter(area_id=area_id)) == 0:
                    raise NoneExistError
                p_consumer = Consumer.objects.get(phone=consumer)
                block = Block.objects.get(area_id=area_id)
                appoint_status = 0
                p = Appointment(content=content, status=appoint_status)
                p.area = block
                p.address = address
                p.name = name
                p.consumer = p_consumer
                pic_url = None
                if pic:
                    pic_name = str(consumer)+str(int(time.time()))
                    path = r'/path/to/store/'+pic_name
                    img = Image.open(pic)
                    img.save(path, "png")
                    pic_url = r'http://path/to/get/'+pic_name
                p.photo = pic_url
                p.save()
                status = 1
        except NoneExistError:
            status = 7
            return HttpResponse(json.dumps({'status': status, 'body': None}))
        except Exception:
            status = 2
            return HttpResponse(json.dumps({'status': status, 'body': None}))
        return HttpResponse(json.dumps({'status': status, 'body': {'pic_url': pic_url}}))


@csrf_exempt
def pull_advertisement(request):
    if request.method == 'GET':
        try:
            if len(Advertisement.objects.all()) == 0:
                raise NoneExistError
            p = Advertisement.objects.all()[0]
            content = p.content
            photo = p.photo
            status = 1
        except NoneExistError:
            status = 7
            return HttpResponse(json.dumps({'status': status, 'body': None}))
        except Exception:
            status = 2
            return HttpResponse(json.dumps({'status': status, 'body': None}))
        return HttpResponse(json.dumps({'status': status, 'body': {'content': content, 'photo': photo}}))


@csrf_exempt
def get_the_full_corresponding(request):
    if request.method == 'GET':
        try:
            querylist = Block.objects.all()
            blocklist = {}
            for p in querylist:
                blocklist[p.area_id] = {'area_id': p.area_id, 'area_name': p.area_name, 'area_tel': p.area_tel}
            status = 1
        except Exception:
            status = 2
            return HttpResponse(json.dumps({'status': status, 'body': None}))
        return HttpResponse(json.dumps({'status': status, 'body': blocklist}))


@csrf_exempt
def test_block(request):
    try:
        req = json.loads(request.body)
        area_id = int(req['area_id'])
        area_tel = req['area_tel']
        area_name = req['area_name']
        area_address = req['area_address']
        area_info = req['area_info']
        status = add_block(area_id=area_id, area_tel=area_tel, area_name=area_name, area_address=area_address, area_info=area_info)
        return HttpResponse(json.dumps({'status': status, 'body': None}))
    except Exception:
        status = 2
    return HttpResponse(json.dumps({'status': status, 'body': None}))
    # req = json.loads(request.body)
    # area_id = req['area_id']
    # status = del_block(area_id)
    # return HttpResponse(json.dumps({'status': status, 'body': None}))


@csrf_exempt
def getnearest(request):
    if request.method == 'GET':
        try:
            lng = request.GET['lng']
            lat = request.GET['lat']
            r_status = getTheNearestFromBaidu(latitude=lat, longitude=lng)
            if r_status['status'] == 2:
                raise Exception
            p = Block.objects.get(baidu_id=r_status['baidu_id'])
            nearest_id = p.area_id
        except Exception:
            return HttpResponse(json.dumps({'status': 2, 'body': None}))
        return HttpResponse(json.dumps({'status': 1, 'body': {'area_id': nearest_id}}))

