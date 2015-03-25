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
from HomeApi.OnlinePay import *
from HomeApi.location_process import *
from django.utils.timezone import utc
import copy
import socket


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
            try:
                verify = Verify.objects.get(phone=phone)
                verify.verify_res = verify_res['verify_code']
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
        raise Http404

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
        raise Http404

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
        raise Http404

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
        raise Http404

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
        raise Http404

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
        raise Http404

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
        raise Http404

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
        raise Http404


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
        raise Http404


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
        raise Http404

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
def get_goods_detail(req):
    body={}
    if req.method == 'POST':
        resjson = simplejson.loads(req.body)
        sid = resjson['sid']
        goods_list = GoodsItem.objects.filter(id=sid)
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
                    # sitem['material'] = item.material
                    # sitem['made_by'] = item.made_by
                    # sitem['made_in'] = item.made_in
                    # sitem['content'] = item.content
                    # sitem['origin_price'] = item.origin_price
                    # sitem['real_price'] = item.real_price
                    # sitem['repair_price'] = item.repair_price
                    sitem['picture'] = item.picture
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
    body={}
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
            newappoint = Appointment(order_id=newid, status=1, address=address, area=block, associator=curuser, order_type=1, online_pay=pay)
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
                                           origin_item=goods,
                                           belong=newappoint)
                newordergoods.save()
                good_title = goods.title + '等'
                good_body = good_body + goods.content + '#'
            if submit_price != price_sure:
                newappoint.valid = False
                newappoint.save()
                newappoint.delete()
                body['msg'] = 'submit price wrong'
                return HttpResponse(encodejson(20, body), content_type='application/json')
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
                new_order_item = OrderHomeItem(title=homeit.title,
                                               price=homeit.price,
                                               content=homeit.content,
                                               belong=newappoint,
                                               origin_item=homeit)
                new_order_item.save()
            if not pay:
                newappoint.amount = price_sure
                newappoint.save()
                body['msg'] = 'create off-line order success'
                return HttpResponse(encodejson(1, body), content_type='application/json')
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
                coupon.if_use = True
                coupon_amount = float(coupon.value)
                newappoint.use_coupon = True
                newappoint.order_coupon = coupon
                newappoint.save()
                coupon.save()
            ping_body = {}
            channel = resjson['channel']
            print coupon_amount
            amount = (price_sure - coupon_amount)
            newappoint.amount = amount
            newappoint.save()
            if amount < 0.0:
                amount = 0.0
            print amount
            amount = int(amount * 100)
            # ping_body['order_no:'] = newid
            ping_body['channel'] = channel
            ping_body['amount'] = amount
            ping_body['client_ip'] = get_my_ip()
            ping_body['currency'] = 'cny'
            ping_body['subject'] = good_title
            ping_body['body'] = good_body
            res = create_new_charge(newid, ping_body, curuser)
            # print res
            body['msg'] = 'server create order success, but not sure ping++ create success'
            body['charge_detail'] = res
            return HttpResponse(encodejson(1, body), content_type='application/json')
        else:
            body['msg'] = 'login first before other action'
            return HttpResponse(encodejson(13, body), content_type='application/json')
    else:
        raise Http404



@csrf_exempt
def verify_consumer(req):
    body={}
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
    body={}
    if req.method == 'POST':
        resjson = simplejson.loads(req.body)
        phone = resjson['phone']
        token = resjson['private_token']
        consumer_list = Consumer.objects.filter(phone=phone)
        if consumer_list.exists():
            consumer = consumer_list[0]
            if not consumer.verified:
                body['msg'] = 'phone is not verified'
                return HttpResponse(encodejson(9, body), content_type='application/json')
            else:
                try:
                    ve = Consumer.objects.get(phone=phone, token=token)
                    address = resjson['address']
                    city_num = resjson['city_number']
                    try:
                        city = Block.objects.get(city_num=city_num)
                    except Exception:
                        body['msg'] = 'invalid city number'
                        return HttpResponse(encodejson(7, body), content_type='application/json')
                    newid = create_order_id(pay=False)
                    newappoint = Appointment(status=1, address=address, consumer=ve, order_id=newid, order_type=2, online_pay=False, area=city)
                    newappoint.save()
                    home_item_list = resjson['home_items']
                    for item in home_item_list:
                        hid = item['hid']
                        home_list = HomeItem.objects.filter(id=hid)
                        if not home_list.exists():
                            body['msg'] = 'home item id:' + str(hid) + 'invalid'
                            newappoint.delete()
                            return HttpResponse(encodejson(7, body), content_type='application/json')
                        homeit = home_list[0]
                        new_order_item = OrderHomeItem(title=homeit.title,
                                               price=homeit.price,
                                               content=homeit.content,
                                               belong=newappoint,
                                               origin_item=homeit)
                        new_order_item.save()
                    body['msg'] = 'appointment create success'
                    return HttpResponse(encodejson(1, body), content_type='application/json')
                except Exception:
                    body['msg'] = 'phone is not verified'
                    return HttpResponse(encodejson(9, body), content_type='application/json')
        else:
            newconsumer = Consumer(phone=phone)
            newconsumer.save()
            body['msg'] = 'phone is not verified'
            return HttpResponse(encodejson(9, body), content_type='application/json')



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


def if_in_due(deadline):
    nowt = datetime.datetime.utcnow().replace(tzinfo=utc)
    detla = deadline - nowt
    if detla < datetime.timedelta():
        return False
    else:
        return True