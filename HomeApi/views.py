# -*- coding: utf-8 -*-
from HomeApi.models import *
from HomeApi.method import *
from django.http import HttpResponse,Http404,JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
import simplejson
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

import copy

@csrf_exempt
def send_reg_verify(req):
    if req.method == 'POST':
        jsonres = simplejson.loads(req.body)
        phone = jsonres['phone']
        verify_res = createverfiycode(phone)
        verify_res = simplejson.loads(verify_res)
        if verify_res['success'] is True:
            newverify = Verify(phone=phone, verify=verify_res['verify_code'])
            newverify.save()
            return HttpResponse(encodejson(1, verify_res), content_type='application/json')
        else:
            return HttpResponse(encodejson(2, {}), content_type='application/json')
    else:
        return Http404


@csrf_exempt
def verify_reg(req):
    body={}
    if req.method == 'POST':
        jsonres = simplejson.loads(req.body)
        phone = jsonres['phone']
        verify_code = jsonres['verify_code']
        verify_list = Verify.objects.filter(phone=phone, verify=str(verify_code))
        if verify_list.count() > 0:
            body['msg'] = 'success'
            return HttpResponse(encodejson(1, body), content_type='application/json')
        else:
            body['msg'] = 'verify failed'
            return HttpResponse(encodejson(7, body), content_type='application/json')
    else:
        return Http404


@csrf_exempt
def register(req):
    body={}
    if req.method =='POST':
        jsonres = simplejson.loads(req.body)
        username = jsonres['username']
        passwd = jsonres['password']
        address = jsonres['address']
        sex = jsonres['sex']
        birthday = jsonres['birthday']
        ishave = Associator.objects.filter(username=username)
        if ishave.count()>0:
            body['msg'] = 'username has exist'
            return HttpResponse(encodejson(6, body), content_type='application/json')
        birthday_datetime = string_to_datetime(birthday)
        passwd = hashlib.md5(passwd).hexdigest()
        token = createtoken()
        newass = Associator(username=username, password=passwd, birthday=birthday_datetime, address=address, sex=sex)
        invite_code = create_invite_code()
        newass.invite_code = invite_code
        newass.private_token = token
        newass.save()
        body['msg'] = 'register success'
        body['phone'] = username
        body['private_token'] = token
        body['invite_code'] = invite_code
        return HttpResponse(encodejson(1,body), content_type='application/json')
    else:
        return Http404

@csrf_exempt
def change_password(req):
    body={}
    if req.method == 'POST':
        jsonres = simplejson.loads(req.body)
        username = jsonres['username']
        old_password = jsonres['old_password']
        new_password = jsonres['new_password']
        token = jsonres['private_token']
        if if_legal(username, token):
            curuser = Associator.objects.get(username=username)
            if curuser.check_password(old_password):
                curuser.password = hashlib.md5(new_password).hexdigest()
                curuser.save()
                body['msg'] = 'change password success'
                return HttpResponse(encodejson(1, body), content_type='application/json')
            else:
                body['msg'] = 'old password is not right'
                return HttpResponse(encodejson(4, body), content_type='application/json')
        else:
            body['msg'] = 'login first before other action'
            return HttpResponse(encodejson(13, body), content_type='application/json')

@csrf_exempt
def login(req):
    body={}
    if req.method == 'POST':
        jsonres = simplejson.loads(req.body)
        username = jsonres['username']
        passwd = jsonres['password']
        user_list = Associator.objects.filter(username=username)
        if user_list.count() == 0:
            body['msg'] = "don't have this user, sign up first"
            return HttpResponse(encodejson(7, body), content_type='application/json')
        else:
            user = user_list[0]
            if user.check_password(passwd):
                newtoken = createtoken()
                user.private_token = newtoken
                user.save()
                body['private_token'] = newtoken
                body['msg'] = 'login success'
                body['username'] = username
                body['invite_code'] = user.invite_code
                return HttpResponse(encodejson(1, body), content_type='application/json')
            else:
                body['msg'] = 'password is not right'
                return HttpResponse(encodejson(4, body), content_type='application/json')
    else:
        return Http404

@csrf_exempt
def logout(req):
    body={}
    if req.method == 'POST':
        jsonres = simplejson.loads(req.body)
        username = jsonres['username']
        token = jsonres['private_token']
        if if_legal(username, token):
            curuser = Associator.objects.get(username=username)
            curuser.private_token = ''
            curuser.save()
            body['msg'] = 'log out success'
            return HttpResponse(encodejson(1, body), content_type='application/json')
        else:
            body['msg'] = 'login first before other action'
            return HttpResponse(encodejson(13, body), content_type='application/json')
    else:
        return Http404

@csrf_exempt
def forget_password(req):
    body = {}
    if req.method == 'POST':
        jsonres = simplejson.loads(req.body)
        phone = jsonres['phone']
        user_list = Associator.objects.filter(username=phone)
        if user_list.count() == 0:
            body['msg'] = 'account does not exist, please sign up'
            return HttpResponse(encodejson(7, body), content_type='application/json')
        res = createverfiycode(phone)
        jres = simplejson.loads(res)
        if jres['success'] is True:
            body['test'] = jres
            body['msg'] = 'verify code send success'
            verify = jres['verify_code']
            newverify = Verify(phone=phone, verify=verify)
            newverify.save()
            return HttpResponse(encodejson(1, body), content_type='application/json')
        else:
            body['msg'] = 'verify code send fail'
            body['test'] = jres
            return HttpResponse(encodejson(2, body), content_type='application/json')
    else:
        return Http404

@csrf_exempt
def reset_password(req):
    body={}
    if req.method == 'POST':
        jsonres = simplejson.loads(req.body)
        verify = jsonres['verify_code']
        phone = jsonres['phone']
        newpassword = jsonres['new_password']
        print verify
        verify_list = Verify.objects.filter(verify=verify, phone=phone)
        if verify_list.count() > 0:
            user_list = Associator.objects.filter(username=phone)
            if user_list.count() > 0:
                user = user_list[0]
                newtoken = createtoken()
                user.password = hashlib.md5(newpassword).hexdigest()
                user.private_token = newtoken
                user.save()
                ver = verify_list[0]
                ver.delete()
                body['username'] = phone
                body['private_token'] = newtoken
                body['msg'] = 'reset password success'
                return HttpResponse(encodejson(1, body), content_type='application/json')
            else:
                body['msg'] = 'account do not exist'
                return HttpResponse(encodejson(7, body), content_type='application/json')
        else:
            body['msg'] = 'verify code does not exist'
            return HttpResponse(encodejson(12, body), content_type='application/json')
    else:
        return Http404

@csrf_exempt
def get_android_version(req):
    body={}
    android = AppControl.objects.all()[0]
    if android.android_version == '':
        body['msg'] = 'no available version info'
        return HttpResponse(encodejson(7, body), content_type='application/json')
    else:
        body['android_version'] = android.android_version
        body['update_time'] = str(timezone.localtime(android.android_update_time))
        return HttpResponse(encodejson(1, body), content_type='application/json')

@csrf_exempt
def get_ios_version(req):
    body={}
    ios = AppControl.objects.all()[0]
    if ios.ios_version == '':
        body['msg'] = 'no available version info'
        return HttpResponse(encodejson(7, body), content_type='application/json')
    else:
        body['ios_version'] = ios.ios_version
        body['update_time'] = str(timezone.localtime(ios.ios_update_time))
        return HttpResponse(encodejson(1, body), content_type='application/json')

@csrf_exempt
def get_messages(req):
    body={}
    if req.method == 'POST':
        jsonres = simplejson.loads(req.body)
        token = jsonres['private_token']
        username = jsonres['username']
        if if_legal(username, token):
            curuser = Associator.objects.get(username=username)
            message_list = Message.objects.filter(own=curuser)
            messages = []
            for itm in message_list:
                message = {}
                message['content'] = itm.content
                message['create_time'] = str(timezone.localtime(itm.create_time))
                message['deadline'] = str(timezone.localtime(itm.deadline))
                messages.append(copy.copy(message))
            body['messages'] = messages
            return HttpResponse(encodejson(1, body), content_type='application/json')
        else:
            body['msg'] = 'login first before other action'
            return HttpResponse(encodejson(13, body), content_type='application/json')
    else:
        return Http404

@csrf_exempt
def add_message(req):
    body={}
    if req.method == 'POST':
        jsonres = simplejson.loads(req.body)
        token = jsonres['private_token']
        username = jsonres['username']
        content = jsonres['content']
        deadline = jsonres['deadline']
        deadline = string_to_datetime(deadline)
        if if_legal(username, token):
            curuser = Associator.objects.get(username=username)
            newmessage = Message(content=content, own=curuser)
            newmessage.create_time = datetime.datetime.now()
            newmessage.deadline = deadline
            newmessage.save()
            body['msg'] = 'message add success'
            return HttpResponse(encodejson(1, body), content_type='application/json')
        else:
            body['msg'] = 'login first before other action'
            return HttpResponse(encodejson(13, body), content_type='application/json')

@csrf_exempt
def get_coupon(req):
    body={}
    if req.method == 'POST':
        jsonres = simplejson.loads(req.body)
        token = jsonres['private_token']
        username = jsonres['username']
        if if_legal(username, token):
            curuser = Associator.objects.get(username=username)
            coupon_list = Coupon.objects.filter(own=curuser)
            coupons = []
            for itm in coupon_list:
                coupon = {}
                coupon['cou_id'] = itm.cou_id
                coupon['value'] = itm.value
                coupon['if_use'] = itm.if_use
                coupon['type'] = itm.type
                coupon['create_time'] = str(timezone.localtime(itm.create_time))
                coupon['owned_time'] = str(timezone.localtime(itm.owned_time))
                coupon['deadline'] = str(timezone.localtime(itm.deadline))
                coupons.append(copy.copy(coupon))
            body['coupons'] = coupons
            return HttpResponse(encodejson(1, body), content_type='application/json')
        else:
            body['msg'] = 'login first before other action'
            return HttpResponse(encodejson(13, body), content_type='application/json')
    else:
        return Http404

@csrf_exempt
def add_feedback(req):
    body={}
    if req.method == 'POST':
        jsonres = simplejson.loads(req.body)
        phone = jsonres['phone']
        content = jsonres['content']
        newfeedback = Feedback(phone=phone, content=content)
        newfeedback.save()
        body['msg'] = 'feedback add success'
        return HttpResponse(encodejson(1, body), content_type='application/json')
    else:
        return Http404

@csrf_exempt
def city_search(req):
    body={}
    if req.method == 'POST':
        jsonres = simplejson.loads(req.body)
        city_num = jsonres['city_num']
        city_list = Block.objects.filter(city_num=city_num)
        if city_list.count() > 0:
            city = city_list[0]
            scity={}
            scity['city_num'] = city.city_num
            scity['city_name'] = city.area_name
            scity['city_tel'] = city.area_tel
            scity['city_address'] = city.area_address
            scity['city_info'] = city.area_info
            body['city'] = scity
            body['match'] = True
            body['msg'] = 'get city success'
            return HttpResponse(encodejson(1, body), content_type='application/json')
        else:
            match_code = search_neighber(city_num)
            city = Block.objects.all()[match_code]
            scity={}
            scity['city_num'] = city.city_num
            scity['city_name'] = city.area_name
            scity['city_tel'] = city.area_tel
            scity['city_address'] = city.area_address
            scity['city_info'] = city.area_info
            body['city'] = scity
            body['match'] = False
            body['msg'] = 'match resemble city success'
            return HttpResponse(encodejson(1, body), content_type='application/json')
    else:
        return Http404

@csrf_exempt
def change_info(req):
    body={}
    birthdayd = None
    if req.method == 'POST':
        jsonres = simplejson.loads(req.body)
        username = jsonres['username']
        token = jsonres['private_token']
        sex = jsonres['sex']
        address = jsonres['address']
        birthday = jsonres['birthday']
        if birthday != '':
            birthdayd = string_to_datetime(birthday)
        if if_legal(username, token):
            curuser = Associator.objects.get(username=username)
            curuser.sex = sex
            curuser.address = address
            curuser.birthday = birthdayd
            curuser.save()
            body['msg'] = 'change info success'
            return HttpResponse(encodejson(1, body), content_type='application/json')
        else:
            body['msg'] = 'login first before other action'
            return HttpResponse(encodejson(13, body), content_type='application/json')
    else:
        return Http404


@csrf_exempt
def get_invite_coupon(req):
    body={}
    if req.method == 'POST':
        resjson = simplejson.loads(req.body)
        token = resjson['private_token']
        username = resjson['username']
        invite_code = resjson['invite_code']
        if if_legal(username, token):
            curuser = Associator.objects.get(username=username)
            if invite_code == curuser.invite_code:
                body['msg'] = 'you can not exchange your own invite code'
                return HttpResponse(encodejson(14, body), content_type='application/json')
            else:
                invite = Associator.objects.filter(invite_code=invite_code)
                if invite.count() > 0:
                    exchanged_list = str(curuser.invite_str).split(',')
                    if invite_code in exchanged_list:
                        body['msg'] = 'you have exchanged this invite code'
                        return HttpResponse(encodejson(6, body), content_type='application/json')
                    else:
                        if create_new_coupon(5, 1, curuser):
                            if curuser.invite_str == '' or curuser.invite_str is None:
                                curuser.invite_str = invite_code
                            else:
                                invite_str = curuser.invite_str
                                invite_str = invite_str + ',' + invite_code
                                curuser.invite_str = invite_str
                            curuser.save()
                            body['msg'] = 'invite code exchange success'
                            return HttpResponse(encodejson(1, body), content_type='application/json')
                        else:
                            body['msg'] = 'invite code exchange failed'
                            return HttpResponse(encodejson(2, body), content_type='application/json')
                else:
                    body['msg'] = 'no invite code info'
                    return HttpResponse(encodejson(7, body), content_type='application/json')
        else:
            body['msg'] = 'login first before other action'
            return HttpResponse(encodejson(13, body), content_type='application/json')
    else:
        return Http404


def create_new_coupon(value, ctype, own, expire=365):
    have_count = Coupon.objects.filter(type=ctype).count()
    odate = datetime.date.today()
    odate = str(odate).replace('-', '')
    newcou_id = '%s%i%05i' % (odate, ctype, have_count+1)
    owntime = datetime.datetime.now()
    expire_day = datetime.timedelta(expire)
    deadline = owntime + expire_day
    newcoupon = Coupon(cou_id=newcou_id, value=value, type=ctype, own=own, owned_time=owntime, deadline=deadline)
    newcoupon.save()
    return True


def if_legal(username, private_token):
    print username
    print private_token
    ass = Associator.objects.filter(username=username, private_token=private_token)
    if ass.count()>0:
        return True
    else:
        return False



def isactive(lastactivetime, det=600):
    print lastactivetime
    nowt = datetime.datetime.utcnow()
    print nowt
    detla = nowt - lastactivetime
    if detla > datetime.timedelta(seconds=det):
        return False
    else:
        return True


def encodejson(status, body):
    tmpjson = {}
    tmpjson['status'] = status
    tmpjson['body'] = body
    return simplejson.dumps(tmpjson)

def createtoken(count=32):
    return string.join(random.sample('ZYXWVUTSRQPONMLKJIHGFEDCBA1234567890zyxwvutsrqponmlkjihgfedcba+=', count)).replace(" ", "")


def string_to_datetime(timestring, timeformat='%Y-%m-%d'):
    dateres = datetime.datetime.strptime(timestring, timeformat)
    return dateres

def create_invite_code(count=6):
    return string.join(random.sample('ZYXWVUTSRQPONMLKJIHGFEDCBA1234567890', count)).replace(" ", "")


def search_neighber(city_num):
    city_list = Block.objects.all()
    for i in range(5, 0, -1):
        num_list = []
        for itm in city_list:
            num_list.append(itm.city_num[0:i])
        def match(city):
            if city == city_num[0:i]:
                return True
            else:
                return False
        res = map(match, num_list)
        if True in res:
            return res.index(True)
    return 0

