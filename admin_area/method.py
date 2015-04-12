# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.template import RequestContext
from django.core.paginator import Paginator
from django.core.paginator import PageNotAnInteger
from django.core.paginator import EmptyPage
import json
from HomeApi.models import *


def get_item_mes(request):
    if not request.session.get('username'):
        return HttpResponseRedirect('login_in')
    if request.method == 'GET':
        type1 = request.GET.get('type1')
        type2 = request.GET.get('type2')
        item_id = request.GET.get('item_id')
        user_admin = HomeAdmin.objects.get(username=request.session['username'])
        if not type1 and not type2 and not item_id:
            raise Http404
        if type1 == '1':
            home_item_p = HomeItem_P.objects.filter(id=item_id)
            if home_item_p.count() == 0:
                return HttpResponse(json.dumps('None'))
            data = dict()
            data['two'] = home_item_p[0].item_name
            if home_item_p[0].type == 1 and type2 == '11':
                data['one'] = "维修"
            elif home_item_p[0].type == 2 and type2 == '12':
                data['one'] = "安装"
            elif home_item_p[0].type == 3 and type2 == '13':
                data['one'] = "更多服务"
            else:
                data = 'None'
            return HttpResponse(json.dumps(data))
        elif type1 == '2':
            goods = GoodsItem.objects.filter(id=item_id)
            if goods.count() == 0:
                return HttpResponse(json.dumps('None'))
            data = dict()
            data['three'] = goods[0].title
            data['two'] = goods[0].parent_item.item_name
            data['one'] = goods[0].parent_item.parent_item.item_name
            return HttpResponse(json.dumps(data))

