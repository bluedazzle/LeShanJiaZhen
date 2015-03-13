# -*- coding: utf-8 -*-
from HomeApi.models import *
from HomeApi.method import *
from django.http import HttpResponse,Http404,JsonResponse
import simplejson
import datetime

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

def verify_reg(req):
    body={}
    if req.method== 'POST':
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


def register(req):
    body={}
    if req.method=='POST':
        jsonres = simplejson.loads(req.body)
        username = jsonres['username']
        passwd = jsonres['password']
        address = jsonres['address']
        nick = jsonres['nick']
        sex = jsonres['sex']
        birthday = jsonres['birthday']
        ishave = Associator.objects.filter(username=username)
        if ishave.count()>0:
            body['msg'] = 'username has exist'
            return HttpResponse(encodejson(6, body), content_type='application/json')
        birthday_datetime = string_to_datetime(birthday)
        passwd = hashlib.md5(passwd).hexdigest()
        token = createtoken()
        newass = Associator(username=username, password=passwd, birthday=birthday_datetime, address=address, sex=sex, nick=nick)
        newass.invite_code = create_invite_code()
        newass.private_token = token
        newass.save()
        body['msg'] = 'register success'
        body['phone'] = username
        body['private_token'] = token
        return HttpResponse(encodejson(1,body), content_type='application/json')
    else:
        return Http404


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


def login(req):
    body={}
    if req.method='POST':
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
                body['private_token'] = newtoken
                body['msg'] = 'login success'
                body['username'] = username
                return HttpResponse(encodejson(1, body), content_type='application/json')
            else:
                body['msg'] = 'password is not right'
                return HttpResponse(encodejson(4, body), content_type='application/json')
    else:
        return Http404


def logout(req):
    body={}
    if req.method='POST':
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

def forget_password(req):
    body = {}
    if req.method='POST':
        jsonres = simplejson.loads(req.body)
        phone = jsonres['phone']
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


def reset_password(req):
    body={}
    if req.method='POST':
        jsonres = simplejson.loads(req.body)
        verify = jsonres['verify_code']
        phone = jsonres['phone']
        newpassword = jsonres['new_password']
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



def get_android_version(req):
    body={}
    android = AppControl.objects.all()[0]
    if android.android_version is None:
        body['msg'] = 'no available version info'
        return HttpResponse(encodejson(7, body), content_type='application/json')
    else:
        body['android_version'] = android.android_version
        body['update_time'] = android.android_update_time
        return HttpResponse(encodejson(1, body), content_type='application/json')

def get_ios_version(req):
    body={}
    ios = AppControl.objects.all()[0]
    if ios.ios_version is None:
        body['msg'] = 'no available version info'
        return HttpResponse(encodejson(7, body), content_type='application/json')
    else:
        body['ios_version'] = ios.ios_version
        body['update_time'] = ios.ios_update_time
        return HttpResponse(encodejson(1, body), content_type='application/json')

def get_messages(req):
    body={}
    if req.method == 'POST':
        jsonres = simplejson.loads(req.body)
        token = jsonres['private_token']
        username = jsonres['username']
        if if_legal(username, token):
            curuser = Associator.objects.get(username=username)
            message_list = Message.objects.filter(own=curuser)
            body['messages'] = message_list
            return HttpResponse(encodejson(1, body), content_type='application/json')
        else:
            return HttpResponse(encodejson(13, body), content_type='application/json')
    else:
        return Http404

def add_message(req):
    body={}
    if req.method = 'POST':
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
            return HttpResponse(encodejson(13, body), content_type='application/json')


def get_coupon(req):
    body={}
    if req.method = 'POST':
        jsonres = simplejson.loads(req.body)
        token = jsonres['private_token']
        username = jsonres['username']
        if if_legal(username, token):
            curuser = Associator.objects.get(username=username)
            coupon_list = Coupon.objects.filter(own=curuser)
            body['coupons'] = coupon_list
            return HttpResponse(encodejson(1, body), content_type='application/json')
        else:
            return HttpResponse(encodejson(13, body), content_type='application/json')
    else:
        return Http404

def add_feedback(req):
    body={}
    if req.method = 'POST':
        jsonres = simplejson.loads(req.body)
        phone = jsonres['username']
        content = jsonres['content']
        newfeedback = Feedback(phone=phone, content=content)
        newfeedback.save()
        body['msg'] = 'feedback add success'
        return HttpResponse(encodejson(1, body), content_type='application/json')
    else:
        return Http404

def if_legal(username, private_token):
    ass = Associator.objects.filter(username=username, prive_token=private_token)
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