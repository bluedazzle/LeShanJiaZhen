# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response
from django.core.context_processors import csrf
from django.views.decorators.csrf import ensure_csrf_cookie
from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.template import RequestContext
from django.core.paginator import Paginator
from django.core.paginator import PageNotAnInteger
from django.core.paginator import EmptyPage
from django import forms
from HomeApi.models import *
from HomeApi.method import *
import json
import simplejson
import hashlib
import datetime
import time
import os
from PIL import Image
import random
from django.test import TestCase

# Create your tests here.


def create_coupons(request):
    if request.method == 'GET':
        for i in range(0, 1000):
            date_now = time.strftime("%Y%m%d", time.localtime())
            type = random.randint(1, 5)
            coupons = Coupon.objects.order_by('-create_time').filter(type=type)
            if coupons.count() == 0:
                coupon_num = date_now + str(type) + '000001'
            else:
                date_newest = coupons[0].create_time.strftime("%Y%m%d")
                if date_newest == date_now:
                    coupon_num = str(int(coupons[0].cou_id)+1)
                else:
                    coupon_num = date_now + str(type) + '000001'
            coupon_new = Coupon()
            coupon_new.cou_id = coupon_num
            coupon_new.type = type
            coupon_new.value = random.randint(1, 10)
            coupon_new.own = Associator.objects.get(username='15682513909')
            time_now = datetime.datetime.utcnow()
            year = int(time_now.strftime("%Y"))
            month = int(time_now.strftime("%m"))
            day = int(time_now.strftime("%d"))
            hour = int(time_now.strftime("%H"))
            minute = int(time_now.strftime("%M"))
            seconds = int(time_now.strftime("%S"))
            coupon_new.deadline = datetime.datetime(year+1, month, day, hour, minute, seconds)
            coupon_new.save()

        return HttpResponse(json.dumps('OK'))


def create_appointments(request):
    if request.method == 'GET':
        for i in range(0, 100):
            new_appointment = Appointment()
            new_appointment.order_id = str(int(time.time())) + str(i)
            new_appointment.status = 1
            new_appointment.address = u"科研楼B区258"
            new_appointment.name = u"张全蛋"
            new_appointment.area = Block.objects.get(city_num='511100')
            new_appointment.associator = Associator.objects.get(username='15682513909')
            flag_type = random.randint(1, 2)
            if flag_type == 1:
                new_appointment.order_type = 1
            else:
                new_appointment.order_type = 2
            new_appointment.amount = random.uniform(10, 100)
            flag_coupon = random.randint(1, 2)
            if flag_coupon == 1 and flag_type == 1:
                new_appointment.use_coupon = True
                coupons = Coupon.objects.order_by('id').filter(if_use=False)
                if coupons.count() > 0:
                    coupon_id = coupons[0].id
                    coupon_use = Coupon.objects.get(id=coupon_id)
                    new_appointment.use_coupon = True
                    new_appointment.order_coupon = coupon_use
                    coupon_use.if_use = True
                    coupon_use.save()
                    print "OK"

            new_appointment.save()
            if flag_type == 1:
                create_order_goods(new_appointment)
            else:
                create_order_home_item(new_appointment)

        return HttpResponse(json.dumps('OK'))


def create_order_goods(new_appointment):
    order_goods_new = OrderGoods()
    order_goods = GoodsItem.objects.all()
    goods_item_number = order_goods.count()
    goods_item_flag = random.randint(0, goods_item_number-1)
    order_goods_origin = order_goods[goods_item_flag]
    order_goods_new.title = order_goods_origin.title
    order_goods_new.brand = order_goods_origin.brand
    order_goods_new.material = order_goods_origin.material
    order_goods_new.made_in = order_goods_origin.made_in
    order_goods_new.made_by = order_goods_origin.made_by
    order_goods_new.content = order_goods_origin.content
    order_goods_new.plus = order_goods_origin.plus
    order_goods_new.origin_price = order_goods_origin.origin_price
    order_goods_new.real_price = order_goods_origin.real_price
    repair_flag = random.randint(1, 2)
    if repair_flag == 1:
        order_goods_new.use_repair = True
    else:
        order_goods_new.use_repair = False
    order_goods_new.picture = order_goods_origin.picture
    order_goods_new.origin_item = order_goods_origin
    order_goods_new.belong = new_appointment
    order_goods_new.save()
    return True


def create_order_home_item(new_appointment):
    order_homeitem_new = OrderHomeItem()
    home_items = HomeItem.objects.all()
    home_items_flag = random.randint(0, home_items.count()-1)
    home_item_origin = home_items[home_items_flag]
    order_homeitem_new.item_name = home_item_origin.item_name
    order_homeitem_new.origin_item = home_item_origin
    order_homeitem_new.belong = new_appointment
    order_homeitem_new.save()
    return True