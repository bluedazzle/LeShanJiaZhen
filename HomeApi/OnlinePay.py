import pingpp
import simplejson

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
    order_no='1234567890',
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
    print a

def create_new_charge():
    pass

