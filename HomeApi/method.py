# -*- coding: utf-8 -*-
import random
import simplejson
import datetime
import string
from HomeApi.yunpian import *
from HomeApi.models import *

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
    tplvalue = '#code#=' + content + "&#company#=四川亿和网络科技有限公司"
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

