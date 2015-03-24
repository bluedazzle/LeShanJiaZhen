import pingpp
import simplejson
from HomeApi.models import *

APP_ID = 'app_DibTK09SavX9mHmH'
TEST_KEY = 'sk_test_DKmjXPD8ij1GjPyvX9ynzzTG'
LIVE_KEY = ''

def do_charge(req):
    jsonres = simplejson.loads(req.body)
    response_charge = pingpp.Charge.create(api_key=TEST_KEY, **jsonres)

    return response_charge


def retrieve(req):
    pingpp.api_key = TEST_KEY
    ch = pingpp.Charge.retrieve('ch_L8qn10mLmr1GS8e5OODmHaL4')


def test():
    ch = pingpp.Charge.create(
    api_key=TEST_KEY,
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
    form['app'] = dict(id=APP_ID)
    ch = pingpp.Charge.create(api_key=TEST_KEY, order_no=new_id, **form)
    cur_appoint = Appointment.objects.get(order_id=new_id)
    newcharge = OnlineCharge()
    newcharge.pingpp_charge_id = ch.id
    # charge_json = simplejson.loads(ch)
    dateArray = datetime.datetime.utcfromtimestamp(ch['created'])
    newcharge.order_id = ch['order_no']
    newcharge.price = ch['amount']
    newcharge.order_with = cur_appoint
    newcharge.own = curuser
    newcharge.pingpp_create_time = dateArray
    newcharge.save()
    return ch

