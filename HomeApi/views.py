from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import json
from HomeApi.errorType import *
from HomeApi.models import *
import time
from PIL import Image


@csrf_exempt
def pull_block_tel(request):
    try:
        req = json.loads(request.body)
        area_name = req['area_name']
        if len(Block.objects.filter(area_name=area_name)) == 0:
            raise NoneExistError
        tel = Block.objects.get(area_name=area_name).area_tel
        status = 1
    except NoneExistError:
        status = 7
        return HttpResponse(json.dumps({'status': status, 'body': None}))
    except Exception:
        status = 2
        return HttpResponse(json.dumps({'status': status, 'body': None}))
    return HttpResponse(json.dumps({'status': status, 'body': {'tel': tel}}))


@csrf_exempt
def make_appointment(request):
    try:
        req = request.POST
        pic = request.FILES.get('file')
        content = req['content']
        process_by = req['process_by']
        consumer = int(req['consumer'])
        if len(Consumer.objects.filter(phone=consumer)) == 0:
            status = 13
            return HttpResponse(json.dumps({'status': status, 'body': None}))
        else:
            if len(HomeAdmin.objects.filter(username=process_by)) == 0:
                raise NoneExistError
            p_consumer = Consumer.objects.get(phone=consumer)
            p_process_by = HomeAdmin.objects.get(username=process_by)
            appoint_status = 0
            p = Appointment(content=content, status=appoint_status)
            p.process_by = p_process_by
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
