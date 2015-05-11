# -*- coding: utf-8 -*-
from HomeApi.models import *
from HomeApi.method import *
from django.http import HttpResponse, Http404, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
import simplejson
import datetime
from PIL import Image
from HomeApi.HomeAdminManager import *
from HomeApi.message import *
from HomeApi.OnlinePay import *
from django.core.serializers import serialize, deserialize
from django.utils.timezone import utc
from django.core.paginator import Paginator
from django.core.paginator import PageNotAnInteger
from django.core.paginator import EmptyPage
import copy
import time
import socket
import os
import math


pathToStorePicture = os.path.dirname(os.path.dirname(__file__))
# pathToGetPicture = r'http://www.kuailejujia.com/uploadpicture/'

@csrf_exempt
def send_reg_verify(req):
    if req.method == 'POST':
        jsonres = simplejson.loads(req.body)
        phone = jsonres['phone']
        verify_res = createverfiycode(phone)
        verify_res = simplejson.loads(verify_res)
        if verify_res['success'] is True:
            try:
                verify = Verify.objects.get(phone=phone)
                verify.verify = verify_res['verify_code']
                verify.save()
            except Exception:
                newverify = Verify(phone=phone, verify=verify_res['verify_code'])
                newverify.save()
            return HttpResponse(encodejson(1, verify_res), content_type='application/json')
        else:
            return HttpResponse(encodejson(2, {}), content_type='application/json')
    else:

        raise Http404


@csrf_exempt
def send_consumer_verify(req):
    if req.method == 'POST':
        jsonres = simplejson.loads(req.body)
        phone = jsonres['phone']
        verify_res = createverfiycode(phone)
        verify_res = simplejson.loads(verify_res)
        con_list = Consumer.objects.filter(phone=phone)
        if not con_list.exists():
            newcon = Consumer(phone=phone)
            newcon.save()
        if verify_res['success'] is True:
            try:
                verify = Verify.objects.get(phone=phone)
                verify.verify = verify_res['verify_code']
                verify.save()
            except Exception:
                newverify = Verify(phone=phone, verify=verify_res['verify_code'])
                newverify.save()
            return HttpResponse(encodejson(1, verify_res), content_type='application/json')
        else:
            return HttpResponse(encodejson(2, {}), content_type='application/json')
    else:

        raise Http404


@csrf_exempt
def register(req):
    body = {}
    if req.method == 'POST':
        jsonres = simplejson.loads(req.body)
        username = jsonres['username']
        passwd = jsonres['password']
        verify = jsonres['verify_code']
        if not verify_reg(username, verify):
            body['msg'] = 'verify_code does not exist'
            return HttpResponse(encodejson(7, body), content_type='application/json')
        ishave = Associator.objects.filter(username=username)
        if ishave.count() > 0:
            body['msg'] = 'username has exist'
            return HttpResponse(encodejson(6, body), content_type='application/json')
        # birthday_datetime = string_to_datetime(birthday)
        passwd = hashlib.md5(passwd).hexdigest()
        token = createtoken()
        newass = Associator(username=username, password=passwd)
        invite_code = create_invite_code()
        newass.invite_code = invite_code
        newass.private_token = token
        newass.save()
        body['msg'] = 'register success'
        body['phone'] = username
        body['private_token'] = token
        body['invite_code'] = invite_code
        couponc = CouponControl.objects.all()[0]
        if couponc.reg_money > 0:
            create_new_coupon(couponc.reg_money, 4, newass)
            mes = REG_MES % str(couponc.reg_money)
            create_new_message(mes, newass)
        return HttpResponse(encodejson(1, body), content_type='application/json')
    else:
        raise Http404


@csrf_exempt
def change_password(req):
    body = {}
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
    body = {}
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
        raise Http404


@csrf_exempt
def logout(req):
    body = {}
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
        raise Http404


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
        raise Http404


@csrf_exempt
def reset_password(req):
    body = {}
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
                body['invite_code'] = user.invite_code
                body['msg'] = 'reset password success'
                return HttpResponse(encodejson(1, body), content_type='application/json')
            else:
                body['msg'] = 'account do not exist'
                return HttpResponse(encodejson(7, body), content_type='application/json')
        else:
            body['msg'] = 'verify code does not exist'
            return HttpResponse(encodejson(12, body), content_type='application/json')
    else:
        raise Http404


@csrf_exempt
def get_android_version(req):
    body = {}
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
    body = {}
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
    body = {}
    if req.method == 'POST':
        jsonres = simplejson.loads(req.body)
        token = jsonres['private_token']
        username = jsonres['username']
        if if_legal(username, token):
            curuser = Associator.objects.get(username=username)
            push_mes = Message.objects.filter(type=1)
            message_list = Message.objects.filter(own=curuser)
            message_list = message_list | push_mes
            message_list = message_list.order_by('-create_time')
            total = message_list.count()
            total_page = math.ceil(float(total) / 20.0)
            paginator = Paginator(message_list, 20)
            page_num = 1
            try:
                page_num = int(jsonres['page'])
                # if page_num > total_page:
                # body['msg'] = 'upbond page number'
                #     return HttpResponse(encodejson(1, body), content_type='application/json')
                message_list = paginator.page(page_num)
            except PageNotAnInteger:
                message_list = paginator.page(1)
            except EmptyPage:
                message_list = []
            except:
                pass
            messages = []
            for itm in message_list:
                message = {}
                message['content'] = itm.content
                message['id'] = itm.id
                message['create_time'] = str(timezone.localtime(itm.create_time))
                message['deadline'] = time.mktime(itm.deadline.timetuple())
                message['read'] = itm.read
                messages.append(copy.copy(message))
            body['messages'] = messages
            body['total_page'] = total_page
            body['total'] = total
            body['page'] = page_num
            return HttpResponse(encodejson(1, body), content_type='application/json')
        else:
            body['msg'] = 'login first before other action'
            return HttpResponse(encodejson(13, body), content_type='application/json')
    else:
        raise Http404


@csrf_exempt
def add_message(req):
    body = {}
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
def get_unread_message_count(req):
    body = {}
    if req.method == 'POST':
        jsonres = simplejson.loads(req.body)
        token = jsonres['private_token']
        username = jsonres['username']
        if if_legal(username, token):
            curuser = Associator.objects.get(username=username)
            message_list = Message.objects.filter(own=curuser, read=False)
            body['count'] = message_list.count()
            return HttpResponse(encodejson(1, body), content_type='application/json')
        else:
            body['msg'] = 'login first before other action'
            return HttpResponse(encodejson(13, body), content_type='application/json')
    else:
        raise Http404


@csrf_exempt
def read_message(req):
    body = {}
    if req.method == 'POST':
        jsonres = simplejson.loads(req.body)
        token = jsonres['private_token']
        username = jsonres['username']
        mid = jsonres['mid']
        if if_legal(username, token):
            curuser = Associator.objects.get(username=username)
            message_list = Message.objects.filter(id=mid)
            if not message_list.exists():
                body['msg'] = 'invalid mid'
                return HttpResponse(encodejson(7, body), content_type='application/json')
            message = message_list[0]
            message.read = True
            message.save()
            body['msg'] = 'message status change success'
            return HttpResponse(encodejson(1, body), content_type='application/json')
        else:
            body['msg'] = 'login first before other action'
            return HttpResponse(encodejson(13, body), content_type='application/json')
    else:
        raise Http404


@csrf_exempt
def get_coupon(req):
    body = {}
    if req.method == 'POST':
        jsonres = simplejson.loads(req.body)
        token = jsonres['private_token']
        username = jsonres['username']
        if if_legal(username, token):
            curuser = Associator.objects.get(username=username)
            coupon_list = Coupon.objects.filter(own=curuser).order_by('if_use', '-value', '-create_time')
            total = coupon_list.count()
            total_page = math.ceil(float(total) / 20.0)
            paginator = Paginator(coupon_list, 20)
            page_num = 1
            try:
                page_num = int(jsonres['page'])
                coupon_list = paginator.page(page_num)
            except PageNotAnInteger:
                coupon_list = paginator.page(1)
            except EmptyPage:
                coupon_list = []
            except:
                pass
            coupons = []
            for itm in coupon_list:
                coupon = {}
                coupon['cou_id'] = itm.cou_id
                coupon['value'] = itm.value
                coupon['if_use'] = itm.if_use
                coupon['type'] = itm.type
                coupon['create_time'] = str(timezone.localtime(itm.create_time))
                coupon['owned_time'] = str(timezone.localtime(itm.owned_time))
                coupon['deadline'] = time.mktime(itm.deadline.timetuple())
                coupons.append(copy.copy(coupon))
            body['coupons'] = coupons
            body['total_page'] = total_page
            body['total'] = total
            body['page'] = page_num
            return HttpResponse(encodejson(1, body), content_type='application/json')
        else:
            body['msg'] = 'login first before other action'
            return HttpResponse(encodejson(13, body), content_type='application/json')
    else:
        raise Http404


@csrf_exempt
def add_feedback(req):
    body = {}
    if req.method == 'POST':
        jsonres = simplejson.loads(req.body)
        phone = jsonres['phone']
        content = jsonres['content']
        newfeedback = Feedback(phone=phone, content=content)
        newfeedback.save()
        body['msg'] = 'feedback add success'
        return HttpResponse(encodejson(1, body), content_type='application/json')
    else:
        raise Http404


@csrf_exempt
def city_search(req):
    body = {}
    if req.method == 'POST':
        jsonres = simplejson.loads(req.body)
        city_num = jsonres['city_num']
        city_list = Block.objects.filter(city_num=city_num)
        if city_list.count() > 0:
            city = city_list[0]
            scity = {}
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
            scity = {}
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
        raise Http404


@csrf_exempt
def change_info(req):
    body = {}
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
        raise Http404


@csrf_exempt
def get_invite_coupon(req):
    body = {}
    if req.method == 'POST':
        resjson = simplejson.loads(req.body)
        token = resjson['private_token']
        username = resjson['username']
        invite_code = str(resjson['invite_code']).upper()
        if if_legal(username, token):
            curuser = Associator.objects.get(username=username)
            if invite_code == curuser.invite_code:
                body['msg'] = 'you can not exchange your own invite code'
                return HttpResponse(encodejson(14, body), content_type='application/json')
            else:
                invite = Associator.objects.filter(invite_code=invite_code)
                if invite.count() > 0:
                    inv = invite[0]
                    exchanged_list = str(curuser.invite_str).split(',')
                    if invite_code in exchanged_list:
                        body['msg'] = 'you have exchanged this invite code'
                        return HttpResponse(encodejson(6, body), content_type='application/json')
                    else:
                        couponc = CouponControl.objects.all()[0]
                        if couponc.invite_money <= 0:
                            body['msg'] = 'invite coupon off'
                            return HttpResponse(encodejson(1, body), content_type='application/json')
                        newc = create_new_coupon(int(couponc.invite_money), 1, curuser)
                        if curuser.invite_str == '' or curuser.invite_str is None:
                            curuser.invite_str = invite_code
                        else:
                            invite_str = curuser.invite_str
                            invite_str = invite_str + ',' + invite_code
                            curuser.invite_str = invite_str
                        curuser.save()
                        body['msg'] = 'invite code exchange success'
                        body['cou_id'] = newc.cou_id
                        body['deadline'] = datetime_to_timestamp(newc.deadline)
                        body['value'] = newc.value
                        mes = IN_MES % str(couponc.invite_money)
                        create_new_message(mes, curuser)
                        create_new_coupon(int(couponc.invite_money), 1, inv)
                        mes = INV_MES % str(couponc.invite_money)
                        create_new_message(mes, inv)
                        return HttpResponse(encodejson(1, body), content_type='application/json')
                else:
                    body['msg'] = 'no invite code info'
                    return HttpResponse(encodejson(7, body), content_type='application/json')
        else:
            body['msg'] = 'login first before other action'
            return HttpResponse(encodejson(13, body), content_type='application/json')
    else:
        raise Http404


@csrf_exempt
def get_goods_p_item(req):
    body = {}
    if req.method == 'POST':
        resjson = simplejson.loads(req.body)
        city_num = resjson['city_number']
        block_list = Block.objects.filter(city_num=city_num)
        if block_list.count() > 0:
            block = block_list[0]
            goods_p_list = Goods_P.objects.filter(area=block)
            goodslist = []
            for itm in goods_p_list:
                goodsp = {}
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
        raise Http404


@csrf_exempt
def get_goods(req):
    body = {}
    if req.method == 'POST':
        resjson = simplejson.loads(req.body)
        goods_id = resjson['pid']
        goods_id_list = Goods_P.objects.filter(id=goods_id).order_by('sort_id')
        if goods_id_list.count() > 0:
            goodpitem = goods_id_list[0]
            goods_o_list = Goods_O.objects.filter(parent_item=goodpitem).order_by('sort_id')
            goodslist = []
            for itm in goods_o_list:
                oitem = {}
                itemlist = GoodsItem.objects.filter(parent_item=itm).order_by('sort_id')
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
                    sitem['icon'] = item.icon
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


@csrf_exempt
def get_goods_p_item(req):
    body = {}
    if req.method == 'POST':
        resjson = simplejson.loads(req.body)
        city_num = resjson['city_number']
        block_list = Block.objects.filter(city_num=city_num)
        if block_list.count() > 0:
            block = block_list[0]
            goods_p_list = Goods_P.objects.filter(area=block).order_by('sort_id')
            goodslist = []
            for itm in goods_p_list:
                goodsp = {}
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
def get_goods_detail(req):
    body = {}
    if req.method == 'POST':
        resjson = simplejson.loads(req.body)
        sid = resjson['sid']
        goods_list = GoodsItem.objects.filter(id=sid).order_by('sort_id')
        if goods_list.count() > 0:
            goods = goods_list[0]
            body['title'] = goods.title
            body['sid'] = goods.id
            body['material'] = goods.material
            body['made_by'] = goods.made_by
            body['made_in'] = goods.made_in
            body['content'] = goods.content
            body['origin_price'] = goods.origin_price
            body['real_price'] = goods.real_price
            body['repair_price'] = goods.repair_price
            body['picture'] = goods.picture
            body['brand'] = goods.brand
            body['icon'] = goods.icon
            body['plus'] = goods.plus
            body['msg'] = 'goods detail get success'
            return HttpResponse(encodejson(1, body), content_type='application/json')
        else:
            body['msg'] = 'invalid sid'
            return HttpResponse(encodejson(7, body), content_type='application/json')
    else:
        raise Http404


@csrf_exempt
def get_goods_o_item(req):
    body = {}
    if req.method == 'POST':
        resjson = simplejson.loads(req.body)
        goods_id = resjson['pid']
        goods_id_list = Goods_P.objects.filter(id=goods_id).order_by('sort_id')
        if goods_id_list.count() > 0:
            goodpitem = goods_id_list[0]
            goods_o_list = Goods_O.objects.filter(parent_item=goodpitem).order_by('sort_id')
            goodslist = []
            for itm in goods_o_list:
                oitem = {}
                itemlist = GoodsItem.objects.filter(parent_item=itm).order_by('sort_id')
                s_itemlist = []
                for item in itemlist:
                    sitem = {}
                    sitem['title'] = item.title
                    sitem['sid'] = item.id
                    # sitem['material'] = item.material
                    # sitem['made_by'] = item.made_by
                    # sitem['made_in'] = item.made_in
                    # sitem['content'] = item.content
                    # sitem['origin_price'] = item.origin_price
                    # sitem['real_price'] = item.real_price
                    # sitem['repair_price'] = item.repair_price
                    sitem['picture'] = item.icon
                    # sitem['brand'] = item.brand
                    # sitem['plus'] = item.plus
                    s_itemlist.append(copy.copy(sitem))
                oitem['item_name'] = itm.item_name
                oitem['oid'] = itm.id
                oitem['s_item_list'] = s_itemlist
                goodslist.append(copy.copy(oitem))
            body['goods'] = goodslist
            body['pid'] = goodpitem.id
            body['msg'] = 'goods item_o get success'
            return HttpResponse(encodejson(1, body), content_type='application/json')
        else:
            body['msg'] = 'invalid goods pid'
            return HttpResponse(encodejson(7, body), content_type='application/json')
    else:
        raise Http404


@csrf_exempt
def create_pay_order(req):
    body = {}
    good_title = ''
    good_body = ''
    if req.method == 'POST':
        resjson = simplejson.loads(req.body)
        username = resjson['username']
        token = resjson['private_token']
        if if_legal(username, token):
            curuser = Associator.objects.get(username=username)
            address = resjson['address']
            city_num = resjson['city_number']
            pay = bool(resjson['online_pay'])
            send_type = resjson['send_type']
            order_phone = resjson['order_phone']
            name = resjson['name']
            use_coupon = bool(resjson['use_coupon'])
            coupon_id = ''
            print use_coupon
            if use_coupon:
                coupon_id = resjson['coupon_id']
            block_list = Block.objects.filter(city_num=city_num)
            if not block_list.exists():
                body['msg'] = 'invalid city_number'
                return HttpResponse(encodejson(7, body), content_type='application/json')
            block = block_list[0]
            newid = create_order_id()
            newappoint = Appointment(order_id=newid,
                                     status=1,
                                     address=address,
                                     send_type=send_type,
                                     area=block,
                                     associator=curuser,
                                     order_type=1,
                                     online_pay=pay,
                                     order_phone=order_phone,
                                     name=name)
            newappoint.save()
            goodslist = resjson['goods_items']
            submit_price = float(resjson['submit_price'])
            price_sure = 0.0
            for item in goodslist:
                sid = item['sid']
                userepair = item['use_repair']
                goodsitems = GoodsItem.objects.filter(id=sid)
                if not goodsitems.exists():
                    body['msg'] = 'goods id:' + str(sid) + 'invalid'
                    newappoint.valid = False
                    newappoint.save()
                    newappoint.delete()
                    return HttpResponse(encodejson(7, body), content_type='application/json')
                goods = goodsitems[0]
                if goods.parent_item.parent_item.area != block:
                    body['msg'] = 'pid does not match city_num'
                    newappoint.delete()
                    return HttpResponse(encodejson(9, body), content_type='application/json')
                price_sure += float(goods.real_price)
                if userepair:
                    price_sure += float(goods.repair_price)
                newordergoods = OrderGoods(title=goods.title,
                                           brand=goods.brand,
                                           material=goods.material,
                                           made_by=goods.made_by,
                                           made_in=goods.made_in,
                                           content=goods.content,
                                           origin_price=goods.origin_price,
                                           real_price=goods.real_price,
                                           repair_price=goods.repair_price,
                                           use_repair=userepair,
                                           picture=goods.picture,
                                           icon=goods.icon,
                                           origin_item=goods,
                                           belong=newappoint)
                newordergoods.save()
                utitle = goods.title[0:8] + '等'
                good_title = utitle
                good_body = good_title
            if send_type == 1:
                if price_sure < 20.0:
                    price_sure += 5
            coupon_amount = 0.0
            if use_coupon:
                coupon_list = Coupon.objects.filter(cou_id=coupon_id)
                if not coupon_list.exists():
                    newappoint.valid = False
                    newappoint.save()
                    newappoint.delete()
                    body['msg'] = 'coupon invalid'
                    return HttpResponse(encodejson(7, body), content_type='application/json')
                coupon = coupon_list[0]
                print coupon.cou_id
                if not (coupon.if_use is False and coupon.own == curuser and if_in_due(coupon.deadline)):
                    newappoint.valid = False
                    newappoint.save()
                    newappoint.delete()
                    body['msg'] = 'the coupon has used, over due or is not belong you'
                    return HttpResponse(encodejson(21, body), content_type='application/json')
                # coupon.if_use = True
                coupon_amount = float(coupon.value)
                newappoint.use_coupon = True
                newappoint.order_coupon = coupon
                newappoint.save()
                # coupon.save()
            ping_body = {}
            channel = resjson['channel']
            print coupon_amount
            amount = (price_sure - coupon_amount)
            newappoint.amount = amount
            newappoint.save()
            if amount < 0.0:
                amount = 0.0
            print amount
            if submit_price != amount:
                newappoint.valid = False
                newappoint.save()
                newappoint.delete()
                body['msg'] = 'submit price wrong'
                return HttpResponse(encodejson(20, body), content_type='application/json')
            amount = int(amount * 100)
            home_item_list = resjson['home_items']
            for item in home_item_list:
                hid = item['hid']
                home_list = HomeItem.objects.filter(id=hid)
                if not home_list.exists():
                    body['msg'] = 'home item id:' + str(hid) + 'invalid'
                    newappoint.valid = False
                    newappoint.save()
                    newappoint.delete()
                    return HttpResponse(encodejson(7, body), content_type='application/json')
                homeit = home_list[0]
                new_order_item = OrderHomeItem(item_name=homeit.item_name,
                                               create_time=datetime.datetime.now(),
                                               belong=newappoint,
                                               origin_item=homeit)
                new_order_item.save()
            # if use_coupon:
            # coupon = Coupon.objects.get(cou_id=coupon_id)
            #     coupon.if_use = True
            #     coupon.save()
            if not pay:
                newappoint.amount = (amount / 100)
                newappoint.valid = True
                newappoint.save()
                body['msg'] = 'create off-line order success'
                return HttpResponse(encodejson(1, body), content_type='application/json')
            # ping_body['order_no:'] = newid
            ping_body['channel'] = channel
            ping_body['amount'] = amount
            ping_body['client_ip'] = get_my_ip()
            ping_body['currency'] = 'cny'
            ping_body['subject'] = good_title
            ping_body['body'] = good_body
            if amount == 0:
                body['msg'] = 'amount is 0,local order create success'
                body['charge_detail'] = False
                body['order_id'] = newid
                return HttpResponse(encodejson(1, body), content_type='application/json')
            res = create_new_charge(newid, ping_body, curuser)
            # print res
            body['msg'] = 'server create order success, but not sure ping++ create success'
            body['charge_detail'] = res
            body['order_id'] = newid
            newappoint.valid = False
            newappoint.save()
            couponc = CouponControl.objects.all()[0]
            if couponc.online_active:
                value = random.randint(couponc.online_money_low, couponc.online_money_high)
                newcoupon = create_new_coupon(value, 2, curuser)
                mes = PAY_MES % str(value)
                create_new_message(mes, curuser)
                body['have_coupon'] = True
                body['coupon_value'] = value
            else:
                body['have_coupon'] = False
            return HttpResponse(encodejson(1, body), content_type='application/json')
        else:
            body['msg'] = 'login first before other action'
            return HttpResponse(encodejson(13, body), content_type='application/json')
    else:
        raise Http404


@csrf_exempt
def status_search(req):
    body = {}
    if not req.method == 'POST':
        raise Http404
    resjson = simplejson.loads(req.body)
    order_id = resjson['order_id']
    username = resjson['username']
    token = resjson['private_token']
    if not if_legal(username, token):
        body['msg'] = 'login first before other action'
        return HttpResponse(encodejson(13, body), content_type='application/json')
    order_list = Appointment.objects.filter(order_id=order_id)
    if not order_list.exists():
        body['msg'] = 'invalid order id'
        return HttpResponse(encodejson(7, body), content_type='application/json')
    order = order_list[0]
    if order.amount == 0:
        body['msg'] = 'amount = 0'
        return HttpResponse(encodejson(1, body), content_type='application/json')
    if order.chargeinfo.paid:
        body['paid'] = True
    else:
        body['paid'] = False
    body['msg'] = 'order status get success'
    body['order_id'] = order_id
    return HttpResponse(encodejson(1, body), content_type='application/json')


@csrf_exempt
def verify_consumer(req):
    body = {}
    if req.method == 'POST':
        resjson = simplejson.loads(req.body)
        phone = resjson['phone']
        verify = resjson['verify_code']
        if verify_reg(phone, verify):
            consumer = Consumer.objects.get(phone=phone)
            if consumer.verified:
                body['private_token'] = consumer.token
            else:
                newtoken = createtoken()
                consumer.verified = True
                consumer.token = newtoken
                consumer.save()
                body['private_token'] = newtoken
            body['msg'] = 'verify success'
            return HttpResponse(encodejson(1, body), content_type='application/json')
        else:
            body['msg'] = 'verify fail'
            return HttpResponse(encodejson(13, body), content_type='application/json')
    else:
        raise Http404


@csrf_exempt
def create_appointment(req):
    body = {}
    consumer = None
    if req.method == 'POST':
        resjson = simplejson.loads(req.body)
        phone = resjson['phone']
        order_phone = resjson['order_phone']
        token = resjson['private_token']
        login = bool(resjson['login'])
        if login:
            if not if_legal(phone, token):
                body['msg'] = 'login first before other action'
                return HttpResponse(encodejson(13, body), content_type='application/json')
            consumer = Associator.objects.get(username=phone)
        else:
            consum_list = Consumer.objects.filter(phone=phone)
            if not consum_list.exists():
                newconsumer = Consumer(phone=phone)
                newconsumer.save()
                body['msg'] = 'phone is not verified'
                return HttpResponse(encodejson(9, body), content_type='application/json')
            consum = consum_list[0]
            if not consum.verified:
                body['msg'] = 'phone is not verified'
                return HttpResponse(encodejson(9, body), content_type='application/json')
        # try:
        ve = None
        if not login:
            ve_list = Consumer.objects.filter(phone=phone, token=token)
            if not ve_list.exists():
                body['msg'] = 'consumer token not correct'
                return HttpResponse(encodejson(9, body), content_type='application/json')
            ve = ve_list[0]
        address = resjson['address']
        name = resjson['name']
        note = resjson['note']
        city_num = resjson['city_number']
        use_coupon = bool(resjson['use_coupon'])
        try:
            city = Block.objects.get(city_num=city_num)
        except Exception:
            body['msg'] = 'invalid city number'
            return HttpResponse(encodejson(7, body), content_type='application/json')
        coupon = None
        if use_coupon:
            cid = resjson['coupon_id']
            cou_list = Coupon.objects.filter(cou_id=cid)
            if not cou_list.exists():
                body['msg'] = 'invalid coupon id'
                return HttpResponse(encodejson(7, body), content_type='application/json')
            coupon = cou_list[0]
            print coupon.cou_id
            print coupon.if_use
            if not (coupon.if_use is False and coupon.own.username == consumer.username and if_in_due(coupon.deadline)):
                body['msg'] = 'the coupon has used, over due or is not belong you'
                return HttpResponse(encodejson(21, body), content_type='application/json')
        newid = create_order_id(pay=False)
        newappoint = Appointment(status=1,
                                 order_phone=order_phone,
                                 use_coupon=use_coupon,
                                 address=address,
                                 order_id=newid,
                                 order_type=2,
                                 online_pay=False,
                                 area=city,
                                 name=name,
                                 valid=True,
                                 remark=note)
        if login:
            newappoint.associator = consumer
            newappoint.save()
        else:
            newappoint.consumer = ve
        if use_coupon:
            newappoint.use_coupon = True
            newappoint.order_coupon = coupon
            coupon.if_use = True
            coupon.save()
        newappoint.save()
        home_item_list = resjson['home_items']
        for item in home_item_list:
            hid = item['hid']
            home_list = HomeItem_P.objects.filter(id=hid)
            if not home_list.exists():
                body['msg'] = 'home item id:' + str(hid) + 'invalid'
                newappoint.delete()
                return HttpResponse(encodejson(7, body), content_type='application/json')
            homeit = home_list[0]
            new_order_item = OrderHomeItem(item_name=homeit.item_name,
                                           create_time=datetime.datetime.now(),
                                           belong=newappoint,
                                           origin_item=homeit)
            new_order_item.save()
        body['msg'] = 'appointment create success'
        body['new_id'] = newid
        return HttpResponse(encodejson(1, body), content_type='application/json')
        # except Exception, e:
        # print e
        #     body['msg'] = 'json value missing or consumer token not correct'
        #     return HttpResponse(encodejson(2, body), content_type='application/json')


@csrf_exempt
def get_home_item_p(req):
    body = {}
    if not req.method == 'POST':
        raise Http404
    resjson = simplejson.loads(req.body)
    city_num = resjson['city_number']
    block_list = Block.objects.filter(city_num=city_num)
    if not block_list.exists():
        body['msg'] = 'invalid city number'
        return HttpResponse(encodejson(7, body), content_type='application/json')
    block = Block.objects.get(city_num=city_num)
    homeitemp_list = HomeItem_P.objects.filter(area=block).order_by('sort_id')
    home_items_list = []
    for itm in homeitemp_list:
        homeitem = {}
        homeitem['pid'] = itm.id
        homeitem['item_name'] = itm.item_name
        homeitem['type'] = itm.type
        homeitem['note'] = itm.note
        homeitem['icon'] = itm.icon
        homeitem['sort_id'] = itm.sort_id
        if itm.recommand:
            homeitem['recommand'] = itm.recommand.id
        else:
            homeitem['recommand'] = -1
        home_items_list.append(copy.copy(homeitem))
    body['parent_item_list'] = home_items_list
    body['msg'] = 'get home items success'
    return HttpResponse(encodejson(1, body), content_type='application/json')


@csrf_exempt
def get_home_item(req):
    body = {}
    if not req.method == 'POST':
        raise Http404
    resjson = simplejson.loads(req.body)
    pid = resjson['pid']
    pitems = HomeItem_P.objects.filter(id=pid)
    if not pitems.exists():
        body['msg'] = 'invalid pid'
        return HttpResponse(encodejson(7, body), content_type='application/json')
    pitem = pitems[0]
    homeitem_list = HomeItem.objects.filter(parent_item=pitem).order_by('sort_id')
    home_list = []
    for itm in homeitem_list:
        homeitem = {}
        homeitem['item_name'] = itm.item_name
        homeitem['sort_id'] = itm.sort_id
        homeitem['hid'] = itm.id
        homeitem['pic_url'] = itm.pic_url
        home_list.append(copy.copy(homeitem))
    body['home_items'] = home_list
    body['msg'] = 'get homeitems success'
    return HttpResponse(encodejson(1, body), content_type='application/json')


@csrf_exempt
def get_recommmand_list(req):
    body = {}
    if not req.method == 'POST':
        raise Http404
    resjson = simplejson.loads(req.body)
    pid = resjson['recommand_id']
    goodps = Goods_P.objects.filter(id=pid)
    if not goodps.exists():
        body['msg'] = 'invalid recommand id'
        return HttpResponse(encodejson(7, body), content_type='application/json')
    goodp = goodps[0]
    goods_os = Goods_O.objects.filter(parent_item=goodp)
    gooditems_all = None
    i = 0
    for itm in goods_os:
        gooditems = GoodsItem.objects.filter(parent_item=itm)
        if i == 0:
            gooditems_all = gooditems
        else:
            gooditems_all = gooditems_all | gooditems
        i += 1
    if gooditems_all is None:
        body['msg'] = 'no recommand list'
        body['recommand_list'] = []
        return HttpResponse(encodejson(1, body), content_type='application/json')
    recommand_list = gooditems_all.order_by('recommand')
    rec_list = []
    for item in recommand_list:
        rec = {}
        if int(item.recommand) == 0:
            continue
        rec['title'] = item.title
        rec['recommand'] = item.recommand
        rec['real_price'] = item.real_price
        rec['origin_price'] = item.origin_price
        rec['repair_price'] = item.repair_price
        rec['sid'] = item.id
        rec['picture'] = item.icon
        rec_list.append(copy.copy(rec))
    body['recommand_list'] = rec_list
    body['msg'] = 'recommand list get success'
    return HttpResponse(encodejson(1, body), content_type='application/json')


@csrf_exempt
def get_advertisment(req):
    body = {}
    if not req.method == 'POST':
        raise Http404
    resjson = simplejson.loads(req.body)
    city_num = resjson['city_number']
    block_list = Block.objects.filter(city_num=city_num)
    if not block_list.exists():
        body['msg'] = 'invalid city number'
        return HttpResponse(encodejson(7, body), content_type='application/json')
    block = block_list[0]
    advertisment_list = Advertisement.objects.filter(area=block)
    jsondata = serialize('json', advertisment_list)
    rejson = simplejson.loads(jsondata)
    body['advertisment_list'] = rejson
    body['msg'] = 'advertisment list get success'
    return HttpResponse(encodejson(1, body), content_type='application/json')


@csrf_exempt
def appraise(req):
    body = {}
    if not req.method == 'POST':
        raise Http404
    resjson = simplejson.loads(req.body)
    username = resjson['username']
    token = resjson['private_token']
    if not if_legal(username, token):
        body['msg'] = 'login befor other action'
        return HttpResponse(encodejson(13, body), content_type='application/json')
    order_id = resjson['order_id']
    curuser = Associator.objects.get(username=username)
    appoint_list = Appointment.objects.filter(order_id=order_id, associator=curuser)
    if not appoint_list.exists():
        body['msg'] = 'invalid order id'
        return HttpResponse(encodejson(7, body), content_type='application/json')
    appoint_list = Appointment.objects.filter(order_id=order_id, status=5)
    if appoint_list.exists():
        body['msg'] = 'the order has been canceled'
        return HttpResponse(encodejson(9, body), content_type='application/json')
    appoint_list = Appointment.objects.filter(order_id=order_id, status=6)
    if appoint_list.exists():
        body['msg'] = 'the order has appraised'
        return HttpResponse(encodejson(6, body), content_type='application/json')
    appoint = Appointment.objects.get(order_id=order_id)
    comment = resjson['comment']
    rate = resjson['rate']
    rb1 = bool(resjson['rb1'])
    rb2 = bool(resjson['rb2'])
    rb3 = bool(resjson['rb3'])
    rb4 = bool(resjson['rb4'])
    rb5 = bool(resjson['rb5'])
    rb6 = bool(resjson['rb6'])
    appoint.comment = comment
    appoint.rate = rate
    appoint.rb1 = rb1
    appoint.rb2 = rb2
    appoint.rb3 = rb3
    appoint.rb4 = rb4
    appoint.rb5 = rb5
    appoint.rb6 = rb6
    appoint.if_appraise = True
    appoint.status = 6
    appoint.save()
    body['msg'] = 'appraise success'
    return HttpResponse(encodejson(1, body), content_type='application/json')


@csrf_exempt
def get_orders(req):
    body = {}
    if not req.method == 'POST':
        raise Http404
    resjson = simplejson.loads(req.body)
    username = resjson['username']
    token = resjson['private_token']
    order_type = int(resjson['order_type'])
    if not if_legal(username, token):
        body['msg'] = 'login befor other action'
        return HttpResponse(encodejson(13, body), content_type='application/json')
    curuser = Associator.objects.get(username=username)
    order_list = Appointment.objects.filter(associator=curuser, order_type=order_type, valid=True).order_by(
        '-create_time')
    total = order_list.count()
    total_page = math.ceil(float(total) / 20.0)
    paginator = Paginator(order_list, 20)
    page_num = 1
    try:
        page_num = int(resjson['page'])
        # if page_num > total_page:
        # body['msg'] = 'upbond page number'
        #     return HttpResponse(encodejson(1, body), content_type='application/json')
        order_list = paginator.page(page_num)
    except PageNotAnInteger:
        order_list = paginator.page(1)
    except EmptyPage:
        order_list = []
    except:
        pass
    order_items = []
    for itm in order_list:
        order = {}
        order['create_time'] = datetime_to_string(itm.create_time)
        order['order_phone'] = itm.order_phone
        order['order_id'] = itm.order_id
        order['status'] = itm.status
        order['address'] = itm.address
        order['name'] = itm.name
        order['order_type'] = itm.order_type
        order['online_pay'] = itm.online_pay
        order['send_type'] = itm.send_type
        order['amount'] = itm.amount
        order['use_coupon'] = itm.use_coupon
        if itm.use_coupon:
            order['coupon_id'] = itm.order_coupon.cou_id
            order['coupon_value'] = itm.order_coupon.value
        order['if_appraise'] = itm.if_appraise
        if itm.if_appraise:
            order['comment'] = itm.comment
            order['rate'] = itm.rate
            order['rb1'] = itm.rb1
            order['rb2'] = itm.rb2
            order['rb3'] = itm.rb3
            order['rb4'] = itm.rb4
            order['rb5'] = itm.rb5
            order['rb6'] = itm.rb6
        if itm.order_type == 1 and itm.amount != 0:
            try:
                order['charge_id'] = itm.chargeinfo.pingpp_charge_id
                order['paid'] = itm.chargeinfo.paid
                order['request_refund'] = itm.chargeinfo.request_refund
                order['refund'] = itm.chargeinfo.refund
                order['channel'] = itm.chargeinfo.channel
                goods_list = []
                for item in itm.ordergoods.all():
                    goods = {}
                    goods['title'] = item.title
                    goods['pid'] = item.origin_item.id
                    goods['pic_url'] = item.origin_item.icon
                    goods['real_price'] = item.real_price
                    goods['repair_price'] = item.repair_price
                    goods['use_repair'] = item.use_repair
                    goods['origin_price'] = item.origin_price
                    goods_list.append(copy.copy(goods))
                order['goods_list'] = goods_list
            except Exception:
                continue
        elif itm.amount == 0:
            goods_list = []
            for item in itm.ordergoods.all():
                goods = {}
                goods['title'] = item.title
                goods['pid'] = item.origin_item.id
                goods['pic_url'] = item.origin_item.icon
                goods['real_price'] = item.real_price
                goods['repair_price'] = item.repair_price
                goods['use_repair'] = item.use_repair
                goods['origin_price'] = item.origin_price
                goods_list.append(copy.copy(goods))
            order['goods_list'] = goods_list
        home_items = []
        for item in itm.orderitem.all():
            home_item = {}
            myrecommand = item.origin_item.recommand
            if myrecommand is not None:
                home_item['recommand'] = myrecommand.id
            else:
                home_item['recommand'] = -1
            home_item['item_name'] = item.item_name
            home_item['hid'] = item.origin_item.id
            home_item['note'] = item.origin_item.note
            home_item['pic_url'] = item.origin_item.icon
            home_items.append(copy.copy(home_item))
        order['home_itmes'] = home_items
        order_items.append(copy.copy(order))
    body['order_list'] = order_items
    body['total_page'] = total_page
    body['total'] = total
    body['page'] = page_num
    body['msg'] = 'get order list success'
    return HttpResponse(encodejson(1, body), content_type='application/json')


@csrf_exempt
def cancel_order(req):
    body = {}
    if not req.method == 'POST':
        raise Http404
    resjson = simplejson.loads(req.body)
    username = resjson['username']
    token = resjson['private_token']
    if not if_legal(username, token):
        body['msg'] = 'login befor other action'
        return HttpResponse(encodejson(13, body), content_type='application/json')
    curuser = Associator.objects.get(username=username)
    order_id = resjson['order_id']
    order_list = Appointment.objects.filter(order_id=order_id, associator=curuser)
    if not order_list.exists():
        body['msg'] = 'invalid order id'
        return HttpResponse(encodejson(7, body), content_type='application/json')
    order = order_list[0]
    if order.status != 1:
        body['msg'] = 'the order can not be canceled'
        body['order_status'] = order.status
        return HttpResponse(encodejson(3, body), content_type='application/json')
    if order.use_coupon:
        order.order_coupon.if_use = False
    order.status = 5
    if order.order_type == 1:
        try:
            order.chargeinfo.request_refund = True
            if order.chargeinfo.paid:
                res = refund_order(order.chargeinfo.pingpp_charge_id, 'test', order.chargeinfo.price)
                if res is None:
                    body['msg'] = 'fail'
                    return HttpResponse(encodejson(2, body), content_type='application/json')
                elif res is False:
                    body['msg'] = order.chargeinfo.fefund_fail_mes
                    return HttpResponse(encodejson(0, body), content_type='application/json')
        except Exception, e:
            print e
            pass
    order.save()
    if order.use_couposn:
        try:
            order.order_coupon.save()
        except Exception, e:
            print e
    if order.order_type == 1:
        try:
            order.chargeinfo.save()
        except Exception, e:
            print e
            pass
    body['msg'] = 'order cancel success'
    return HttpResponse(encodejson(1, body), content_type='application/json')


@csrf_exempt
def check_game(req):
    body = {}
    if not req.method == 'POST':
        raise Http404
    resjson = simplejson.loads(req.body)
    username = resjson['username']
    token = resjson['private_token']
    if not if_legal(username, token):
        body['msg'] = 'login befor other action'
        return HttpResponse(encodejson(13, body), content_type='application/json')
    coupon_control = CouponControl.objects.all()[0]
    if coupon_control.game_active:
        curuser = Associator.objects.get(username=username)
        if curuser.game_str == coupon_control.game_sign and curuser.game_times >= coupon_control.game_times:
            body['can_game'] = False
        else:
            body['can_game'] = True
        body['have_game'] = True
        body['msg'] = 'game status get success'
        return HttpResponse(encodejson(1, body), content_type='application/json')
    else:
        body['have_game'] = False
        body['msg'] = 'game status get success'
        return HttpResponse(encodejson(1, body), content_type='application/json')


@csrf_exempt
def play_game(req):
    body = {}
    if not req.method == 'POST':
        raise Http404
    resjson = simplejson.loads(req.body)
    username = resjson['username']
    token = resjson['private_token']
    if not if_legal(username, token):
        body['msg'] = 'login befor other action'
        return HttpResponse(encodejson(13, body), content_type='application/json')
    coupon_control = CouponControl.objects.all()[0]
    if not coupon_control.game_active:
        body['msg'] = 'no game can play'
        return HttpResponse(encodejson(7, body), content_type='application/json')
    if not (not isactive(coupon_control.game_start_time.replace(tzinfo=None), 0) and isactive(
            coupon_control.game_end_time.replace(tzinfo=None), 0)):
        body['msg'] = 'game time not begin or already end'
        return HttpResponse(encodejson(7, body), content_type='application/json')
    if coupon_control.game_current_num == coupon_control.game_coupon_num:
        body['msg'] = 'coupon send over number'
        return HttpResponse(encodejson(7, body), content_type='application/json')
    value = random.randint(coupon_control.game_money_low, coupon_control.game_money_high)
    curuser = Associator.objects.get(username=username)
    if curuser.game_str != coupon_control.game_sign:
        curuser.game_str = coupon_control.game_sign
        curuser.game_times = 0
        curuser.save()
    else:
        if curuser.game_times >= coupon_control.game_times:
            body['msg'] = 'game times upbound'
            return HttpResponse(encodejson(9, body), content_type='application/json')
    newc = create_new_coupon(value, 3, curuser, 365, coupon_control.game_sign)
    curuser.game_times += 1
    curuser.save()
    body['msg'] = 'get coupon success'
    body['value'] = value
    body['cou_id'] = newc.cou_id
    body['deadline'] = datetime_to_timestamp(newc.deadline)
    coupon_control.game_current_num += 1
    coupon_control.save()
    mes = GAME_MES % str(value)
    create_new_message(mes, curuser)
    return HttpResponse(encodejson(1, body), content_type='application/json')


@csrf_exempt
def appointment_pic(request):
    body = {}
    if not request.method == 'POST':
        raise Http404
    req = request.POST
    token = req['token']
    phone = req['phone']
    login = str(req['login']).lower()
    print login
    if login == 'true':
        login = True
    else:
        login = False
    picindex = req['picindex']
    appointment_id = req['appointment_id']
    pic = request.FILES.get('file')
    appoint_list = Appointment.objects.filter(order_id=appointment_id)
    if not appoint_list.exists():
        body['msg'] = 'invalid appointment id'
        return HttpResponse(encodejson(7, body), content_type='application/json')
    curuser = None
    if login:
        if not if_legal(phone, token):
            body['msg'] = 'login before other action'
            return HttpResponse(encodejson(13, body), content_type='application/json')
        curuser = Associator.objects.get(username=phone)
    else:
        consumer_list = Consumer.objects.filter(phone=phone)
        if not consumer_list.exists():
            newconsumer = Consumer(phone=phone)
            newconsumer.save()
            body['msg'] = 'phone is not verified'
            return HttpResponse(encodejson(9, body), content_type='application/json')
        consumer = consumer_list[0]
        if not consumer.verified:
            body['msg'] = 'phone is not verified'
            return HttpResponse(encodejson(9, body), content_type='application/json')
        consumer_list = Consumer.objects.filter(phone=phone, token=token)
        if not consumer_list.exists():
            body['msg'] = 'token is not correct'
            return HttpResponse(encodejson(9, body), content_type='application/json')
        curuser = consumer_list[0]
    appoint = appoint_list[0]
    if not pic:
        body['msg'] = 'no picture'
        return HttpResponse(encodejson(1, body), content_type='application/json')
    pic_name = str(curuser) + str(int(time.time())) + str(random.randint(10000, 99999)) + '.png'
    path = pathToStorePicture + '/upload/' + pic_name
    img = Image.open(pic)
    img.save(path, "png")
    if picindex == '1':
        appoint.photo1 = pic_name
    elif picindex == '2':
        appoint.photo2 = pic_name
    elif picindex == '3':
        appoint.photo3 = pic_name
    elif picindex == '4':
        appoint.photo4 = pic_name
    appoint.save()
    body['msg'] = 'upload picture success'
    return HttpResponse(encodejson(1, body), content_type='application/json')


@csrf_exempt
def get_all_city(req):
    body = {}
    if not req.method == 'GET':
        raise Http404
    block_list = Block.objects.all()
    block_lists = []
    for itm in block_list:
        block = {}
        block['city_number'] = itm.city_num
        block['city_name'] = itm.area_name
        block['city_tel'] = itm.area_tel
        block['city_address'] = itm.area_address
        block['city_info'] = itm.area_info
        block_lists.append(copy.copy(block))
    body['block_list'] = block_lists
    return HttpResponse(encodejson(1, body), content_type='application/json')


def get_my_ip():
    myname = socket.getfqdn(socket.gethostname())
    myaddr = socket.gethostbyname(myname)
    return myaddr


def create_order_id(pay=True):
    odate = datetime.date.today()
    if pay:
        todaynum = int(Appointment.objects.filter(create_time__gte=odate, order_type=1).count()) + 1
    else:
        todaynum = int(Appointment.objects.filter(create_time__gte=odate, order_type=2).count()) + 1
    odate = str(odate).replace('-', '')
    paystr = '00'
    if pay:
        paystr = '01'
    ordernum = '%s%s%08i' % (odate, paystr, todaynum)
    print ordernum
    return ordernum


def create_new_coupon(value, ctype, own, expire=365, gamesign=''):
    if gamesign != '':
        have_count = Coupon.objects.filter(type=ctype, game_sign=gamesign).count()
    else:
        have_count = Coupon.objects.filter(type=ctype).count()
    odate = datetime.date.today()
    odate = str(odate).replace('-', '')
    if gamesign != '':
        newcou_id = '%s%s%i%05i' % (odate, gamesign[0:2], ctype, have_count + 1)
    else:
        newcou_id = '%s%i%05i' % (odate, ctype, have_count + 1)
    owntime = datetime.datetime.now()
    expire_day = datetime.timedelta(expire)
    deadline = owntime + expire_day
    newcoupon = Coupon(cou_id=newcou_id, value=value, type=ctype, own=own, game_sign=gamesign, owned_time=owntime,
                       deadline=deadline)
    try:
        newcoupon.save()
    except:
        return create_new_coupon(value, ctype, own, expire, gamesign)
    return newcoupon


def if_legal(username, private_token):
    print username
    print private_token
    ass = Associator.objects.filter(username=username, private_token=private_token)
    if ass.count() > 0:
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
    return string.join(
        random.sample('ZYXWVUTSRQPONMLKJIHGFEDCBA1234567890zyxwvutsrqponmlkjihgfedcba+=', count)).replace(" ", "")


def string_to_datetime(timestring, timeformat='%Y-%m-%d'):
    dateres = datetime.datetime.strptime(timestring, timeformat)
    return dateres


def datetime_to_timestamp(datetimet):
    return time.mktime(datetimet.timetuple())


def datetime_to_string(datetimet):
    return str(timezone.localtime(datetimet))


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


def if_in_due(deadline):
    nowt = datetime.datetime.utcnow().replace(tzinfo=utc)
    detla = deadline - nowt
    if detla < datetime.timedelta(0):
        return False
    else:
        return True
