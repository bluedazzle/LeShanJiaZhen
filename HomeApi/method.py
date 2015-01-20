# -*- coding: utf-8 -*-
import random
import simplejson
import datetime
import string
from HomeApi.yunpian import *
from HomeApi.models import *
import xinge

def createverfiycode(phone, count=6):
    result = {}
    vercode = string.join(random.sample('0123456789', count)).replace(" ", "")
    res = sendverifycode(vercode, phone)
    result['success'] = res
    result['verify_code'] = vercode
    jsonen = simplejson.dumps(result)
    return jsonen

def sendverifycode(content, phone):
    result_list = PhoneVerify.objects.filter(phone = phone)
    result = None
    if result_list.count() > 0:
        result = result_list[0]
        nowtime = datetime.datetime.utcnow()
        lasttime = result.update_time.replace(tzinfo=None)
        if (nowtime - lasttime) < datetime.timedelta(seconds=30):
            return False
    apikey = 'e1ebef39f28c86fdb57808eb45ab713a'
    tplvalue = '#code#=' + content + "&#company#=快乐居家科技有限责任公司"
    res = tpl_send_sms(apikey, '1', tplvalue, phone)
    jsres = simplejson.loads(res)
    msg = jsres['code']
    print msg
    print result
    if str(msg) == '0':
        if result is not None:
            result.verify = content
            result.update_time = datetime.datetime.now()
            result.save()
        else:
            new_ver = PhoneVerify()
            new_ver.phone = phone
            new_ver.update_time = datetime.datetime.now()
            new_ver.verify = content
            new_ver.save()
        return True
    else:
        print jsres
        return False


def customedPush(msg):
    xios = xinge.XingeApp(2200050216, '2f7f56e61191393d6b25079ee9d839b0')
    ios = xinge.MessageIOS()
    ios.alert = msg
    ios.sound = "default"
    ios.badge = 1
    ios.expireTime = 86400
    ret = xios.PushAllDevices(0, ios, 1)

    xandroid = xinge.XingeApp(2100081128, 'db2f948d8f2b962fc4e1cb4a26f7d87d')
    android =xinge.Message()
    android.type = xinge.Message.TYPE_NOTIFICATION
    android.title = '易修哥'
    android.content = msg
    android.expireTime = 86400
    res = xandroid.PushAllDevices(0,android)

    if ret[0] == 0 and res[0] == 0:
        return True
    else:
        return False

