# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import json
import simplejson
import random
import string
import base64
from HomeApi.errorType import *
from HomeApi.models import *
from HomeApi.method import *
import time
import datetime
from PIL import Image
from HomeApi.HomeAdminManager import *
from HomeApi.location_process import *

pathToStorePicture = r'/var/leshanjiazheng/uploadpicture/'
pathToGetPicture = r'http://115.29.138.80/uploadpicture/'



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
            # pic1 = request.FILES.get('file1')
            # pic2 = request.FILES.get('file2')
            # pic3 = request.FILES.get('file3')
            # pic4 = request.FILES.get('file4')
            content = req['content']
            name = req['name']
            area_id = req['area_id']
            address = req['address']
            token = req['token']
            consumer = req['consumer']
            appoint_time = req['time']
            remark = req['remark']
            if len(Consumer.objects.filter(phone=consumer)) != 0:
                if Consumer.objects.get(phone=consumer).token != token:
                    status = 13
                    return HttpResponse(json.dumps({'status': status, 'body': None}))
                else:
                    if len(Block.objects.filter(area_id=area_id)) == 0:
                        raise NoneExistError
                    p_consumer = Consumer.objects.get(phone=consumer)
                    block = Block.objects.get(area_id=area_id)
                    appoint_status = 1
                    p = Appointment(content=content, status=appoint_status)
                    p.area = block
                    p.address = address
                    p.name = name
                    p.consumer = p_consumer
                    p.appoint_time = datetime.datetime.fromtimestamp(int(appoint_time))
                    p.appointment_id = str(int(time.time()))[:10] + str(consumer)[:4]
                    print p.appointment_id
                    p.remark = remark
                    # if pic1:
                    #     pic_name = str(consumer)+str(int(time.time()))+str(random.randint(10000, 99999))
                    #     path = pathToStorePicture+pic_name
                    #     img = Image.open(pic1)
                    #     img.save(path, "png")
                    #     pic_url = pathToGetPicture+pic_name
                    #     p.photo1 = pic_url
                    # if pic2:
                    #     pic_name = str(consumer)+str(int(time.time()))+str(random.randint(10000, 99999))
                    #     path = pathToStorePicture+pic_name
                    #     img = Image.open(pic2)
                    #     img.save(path, "png")
                    #     pic_url = pathToGetPicture+pic_name
                    #     p.photo2 = pic_url
                    # if pic3:
                    #     pic_name = str(consumer)+str(int(time.time()))+str(random.randint(10000, 99999))
                    #     path = pathToStorePicture+pic_name
                    #     img = Image.open(pic3)
                    #     img.save(path, "png")
                    #     pic_url = pathToGetPicture+pic_name
                    #     p.photo3 = pic_url
                    # if pic4:
                    #     pic_name = str(consumer)+str(int(time.time()))+str(random.randint(10000, 99999))
                    #     path = pathToStorePicture+pic_name
                    #     img = Image.open(pic4)
                    #     img.save(path, "png")
                    #     pic_url = pathToGetPicture+pic_name
                    #     p.photo4 = pic_url
                    p.save()
                    status = 1
            else:
                status = 13
        except NoneExistError:
            status = 7
            return HttpResponse(json.dumps({'status': status, 'body': None}))
        except Exception:
            status = 2
            return HttpResponse(json.dumps({'status': status, 'body': None}))
        return HttpResponse(json.dumps({'status': status, 'body': {'appointmentid': p.appointment_id}}))


@csrf_exempt
def appointment_pic(request):
    if request.method == 'POST':
        try:
            req = request.POST
            token = req['token']
            consumer = req['consumer']
            picindex = req['picindex']
            appointment_id = req['appointmentid']
            pic = request.FILES.get('file')
            if len(Appointment.objects.filter(appointment_id=appointment_id)) != 0:
                if Consumer.objects.get(phone=consumer).token != token:
                    status = 13
                    return HttpResponse(json.dumps({'status': status, 'body': None}))
                else:
                    appoint = Appointment.objects.get(appointment_id=appointment_id)
                    if pic:
                        pic_name = str(consumer)+str(int(time.time()))+str(random.randint(10000, 99999))
                        path = pathToStorePicture+pic_name
                        img = Image.open(pic)
                        img.save(path, "png")
                        pic_url = pathToGetPicture+pic_name
                        # pic_dic = {'1': appoint.photo1, '2': appoint.photo2, '3': appoint.photo3, '4': appoint.photo4}
                        if picindex == '1':
                            appoint.photo1 = pic_url
                        elif picindex == '2':
                            appoint.photo2 = pic_url
                        elif picindex == '3':
                            appoint.photo3 = pic_url
                        elif picindex == '4':
                            appoint.photo4 = pic_url
                        else:
                            raise Exception
                    appoint.save()
                    status = 1
            else:
                status = 13
        except Exception:
            status = 2
        return HttpResponse(json.dumps({'status': status, 'body': None}))


@csrf_exempt
def send_phone_verify(request):
    if request.method == 'POST':
        try:
            phone = request.POST['consumer']
            if len(Consumer.objects.filter(phone=phone)) == 0:
                aaa = string.ascii_letters+'0123456789'
                c_token = base64.encodestring(str(int(time.time()))+''.join(random.sample(aaa, 6))+phone).replace('\n', '')
                p = Consumer()
                p.phone = phone
                p.token = c_token
                p.save()
            #发送验证码，进行验证操作
            result = simplejson.loads(createverfiycode(phone))
            if result['success']:
                #验证码发送成功
                status = 1
            else:
                status = 2
        except Exception:
            status = 2
        return HttpResponse(json.dumps({'status': status, 'body': None}))


@csrf_exempt
def verify_get_token(request):
    if request.method == 'POST':
        try:
            phone = request.POST['consumer']
            vercode = request.POST['vercode']
            delta = (datetime.datetime.utcnow() - PhoneVerify.objects.get(phone=phone).update_time.replace(tzinfo=None)).seconds
            if delta < 600:
                if PhoneVerify.objects.get(phone=phone).verify == int(vercode):
                    token = Consumer.objects.get(phone=phone).token
                    body = [{'token': token}]
                    status = 1
                else:
                    status = 12
                    body = None
            else:
                status = 5
                body = delta
        except Exception:
            status = 2
            body = None
        return HttpResponse(json.dumps({'status': status, 'body': body}))


@csrf_exempt
def pull_advertisement(request):
    if request.method == 'GET':
        try:
            if len(Advertisement.objects.all()) == 0:
                raise NoneExistError
            p = Advertisement.objects.filter(is_new=True)
            body = []
            for ads in p:
                adp = {}
                adp['content'] = ads.content
                adp['photo'] = ads.photo
                body.append(adp)
            status = 1
        except NoneExistError:
            status = 7
            return HttpResponse(json.dumps({'status': status, 'body': None}))
        except Exception:
            status = 2
            return HttpResponse(json.dumps({'status': status, 'body': None}))
        return HttpResponse(json.dumps({'status': status, 'body': body}))


@csrf_exempt
def get_detail_item(request):
    if request.method == 'GET':
        try:
            category_id = request.GET['category_id']
            if len(HomeItem_P.objects.filter(sort_id=category_id)) == 0:
                raise NoneExistError
            itemlist = []
            category = HomeItem_P.objects.get(sort_id=category_id)
            for p in category.homeitem_set.order_by('sort_id'):
                itemlist.append({'item_id': p.sort_id, 'title': p.title, 'content': p.content, 'price': p.price})
            status = 1
        except NoneExistError:
            status = 7
            return HttpResponse(json.dumps({'status': status, 'body': None}))
        except Exception:
            status = 2
            return HttpResponse(json.dumps({'status': status, 'body': None}))
        return HttpResponse(json.dumps({'status': status, 'body': itemlist}))


@csrf_exempt
def get_categories(request):
    if request.method == 'GET':
        try:
            querylist = HomeItem_P.objects.all()
            category_list = []
            for p in querylist:
                category_list.append({'category_id': p.sort_id, 'category': p.item_name, 'url': p.icon})
            status = 1
        except Exception:
            status = 2
            return HttpResponse(json.dumps({'status': status, 'body': None}))
        return HttpResponse(json.dumps({'status': status, 'body': category_list}))


@csrf_exempt
def test_block(request):
    # try:
        req = json.loads(request.body)
        area_id = int(req['area_id'])
        area_tel = req['area_tel']
        area_name = req['area_name']
        area_address = req['area_address']
        area_info = req['area_info']
        status = add_block(area_id=area_id, area_tel=area_tel, area_name=area_name, area_address=area_address, area_info=area_info)
        return HttpResponse(json.dumps({'status': status, 'body': None}))
    # except Exception:
    #     status = 2
    # return HttpResponse(json.dumps({'status': status, 'body': None}))
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


@csrf_exempt
def ger_verify(req):
