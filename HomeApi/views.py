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
import copy


pathToStorePicture = r'/var/leshanjiazheng/uploadpicture/'
pathToGetPicture = r'http://115.29.138.80/uploadpicture/'

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
def register(req):
    body={}
    if req.method =='POST':
        jsonres = simplejson.loads(req.body)
        username = jsonres['username']
        passwd = jsonres['password']
        address = jsonres['address']
        verify = jsonres['verify_code']
        sex = jsonres['sex']
        birthday = jsonres['birthday']
        if not verify_reg(username, verify):
            body['msg'] = 'verify_code does not exist'
            return HttpResponse(encodejson(7, body), content_type='application/json')
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


@csrf_exempt
def get_goods_p_item(req):
    body={}
    if req.method == 'POST':
        resjson = simplejson.loads(req.body)
        city_num = resjson['city_number']
        block_list = Block.objects.filter(city_num=city_num)
        if block_list.count() > 0:
            block = block_list[0]
            goods_p_list = Goods_P.objects.filter(area=block)
            goodslist = []
            for itm in goods_p_list:
                goodsp={}
                goodsp['item_name'] = itm.item_name
                goodsp['pid'] = itm.id
                goodsp['have_advertisment'] = itm.have_advertisment
                goodsp['advertisment'] = itm.advertisement
                goodslist.append(copy.copy(goodsp))
            body['goods_item'] = goodslist
            body['msg'] = 'goods_p get success'
            return HttpResponse(encodejson(1, body), content_type='application/json')
        else:
            body['msg'] = 'invalid city number'
            return HttpResponse(encodejson(7, body), content_type='application/json')
    else:
        return Http404

@csrf_exempt
def get_goods(req):
    body={}
    if req.method == 'POST':
        resjson = simplejson.loads(req.body)
        goods_id = resjson['pid']
        goods_id_list = Goods_P.objects.filter(id=goods_id)
        if goods_id_list.count() > 0:
            goodpitem = goods_id_list[0]
            goods_o_list = Goods_O.objects.filter(parent_item=goodpitem)
            goodslist = []
            for itm in goods_o_list:
                oitem= {}
                itemlist = GoodsItem.objects.filter(parent_item=itm)
                s_itemlist = []
                for item in itemlist:
                    sitem = {}
                    sitem['title'] = item.title
                    sitem['sid'] = item.id
                    sitem['material'] = item.material
                    sitem['made_by'] = item.made_by
                    sitem['made_in'] = item.made_in
                    sitem['content'] = item.content
                    sitem['origin_price'] = item.origin_price
                    sitem['real_price'] = item.real_price
                    sitem['repair_price'] = item.repair_price
                    sitem['picture'] = item.picture
                    sitem['brand'] = item.brand
                    sitem['plus'] = item.plus
                    s_itemlist.append(copy.copy(sitem))
                oitem['item_name'] = itm.item_name
                oitem['oid'] = itm.id
                oitem['s_item_list'] = s_itemlist
                goodslist.append(copy.copy(oitem))
            body['goods'] = goodslist
            body['pid'] = goodpitem.id
            body['msg'] = 'goods detail get success'
            return HttpResponse(encodejson(1, body), content_type='application/json')
        else:
            body['msg'] = 'invalid goods pid'
            return HttpResponse(encodejson(7, body), content_type='application/json')
    else:
        raise Http404



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

def verify_reg(phone, verify_code):
        verify_list = Verify.objects.filter(phone=phone, verify=str(verify_code))
        if verify_list.count() > 0:
            verify = verify_list[0]
            verify.delete()
            return True
        else:
            return False