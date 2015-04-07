# -*- coding: utf-8 -*-
import pingpp
import simplejson
import datetime
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from HomeApi.models import *

APP_ID = 'app_DibTK09SavX9mHmH'
LIVE_KEY = 'sk_test_DKmjXPD8ij1GjPyvX9ynzzTG'
# LIVE_KEY = 'sk_live_fBZKaXibpI0xkf6IIjdqkubL'

def do_charge(req):
    jsonres = simplejson.loads(req.body)
    response_charge = pingpp.Charge.create(api_key=LIVE_KEY, **jsonres)

    return response_charge


def retrieve(req):
    pingpp.api_key = LIVE_KEY
    ch = pingpp.Charge.retrieve('ch_L8qn10mLmr1GS8e5OODmHaL4')


def test():
    ch = pingpp.Charge.create(
    api_key=LIVE_KEY,
    amount=1,
    app=dict(id=APP_ID),
    channel='upmp',
    currency='cny',
    client_ip='127.0.0.1',
    subject='test-subject',
    body='test-body',)
    print type(ch)

    # print ch.items()
    a = simplejson.dumps(ch)
    return ch

def create_new_charge(new_id, form, curuser):
    # print form['amount']
    form['app'] = dict(id=APP_ID)
    ch = pingpp.Charge.create(api_key=LIVE_KEY, order_no=new_id, **form)
    cur_appoint = Appointment.objects.get(order_id=new_id)
    newcharge = OnlineCharge()
    newcharge.pingpp_charge_id = ch.id
    # charge_json = simplejson.loads(ch)
    # print ch['amount']
    dateArray = datetime.datetime.fromtimestamp(ch['created'])
    expire = datetime.datetime.fromtimestamp(ch['time_expire'])
    newcharge.order_id = ch['order_no']
    newcharge.channel = ch['channel']
    newcharge.price = ch['amount']
    newcharge.time_expire = expire
    newcharge.order_with = cur_appoint
    newcharge.own = curuser
    newcharge.pingpp_create_time = dateArray
    newcharge.save()
    return ch


@csrf_exempt
def charge_result(req):
    notify = simplejson.loads(req.body)
    if 'object' not in notify:
      return HttpResponse('fail')
    else:
      if notify['object'] == 'charge':
        # 开发者在此处加入对支付异步通知的处理代码
        charge_id = notify['id']
        paid = bool(notify['paid'])
        online_charge = OnlineCharge.objects.get(pingpp_charge_id=charge_id)
        if paid:
            online_charge.paid = True
            online_charge.save()
        print 'success'
        return HttpResponse('success')
      elif notify['object'] == 'refund':
        # 开发者在此处加入对退款异步通知的处理代码
        refund_id = notify['id']
        id = notify['charge']
        online_charge = OnlineCharge.objects.get(pingpp_charge_id=id)
        online_charge.refund = True
        online_charge.refund_id = refund_id
        online_charge.save()
        print 'success'
        return HttpResponse('success')
      else:
        print 'fail'
        return HttpResponse('fail')


def refund_order(order_id, description, amount):
    pingpp.api_key = LIVE_KEY
    ch = pingpp.Charge.retrieve(order_id)
    re = ch.refunds.create(description=description, amount=amount)
    # print '233333'
    # print re
    # print re['object']
    # print '233333'
    if re['object'] == 'refund':
        refund_o = OnlineCharge.objects.get(pingpp_charge_id=order_id)
        refund_o.refund_id = re['id']
        refund_o.refund = re['succeed']
        refund_o.refund_desc = re['description']
        refund_o.refund_fail_mes = re['failure_msg']
        refund_o.save()
    else:
        return None
    if re['succeed']:
        return True
    else:
        return False