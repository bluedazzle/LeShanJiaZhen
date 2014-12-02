from django.shortcuts import render_to_response
from django.core.context_processors import csrf
from django.views.decorators.csrf import ensure_csrf_cookie
from django.http import HttpResponseRedirect
from django.template import RequestContext
from django.core.paginator import Paginator
from django.core.paginator import PageNotAnInteger
from django.core.paginator import EmptyPage
from HomeApi.models import *
import json
import simplejson
import hashlib
import datetime


def login_in(request):
    if request.method == 'GET':
        return render_to_response('login_in.html', context_instance=RequestContext(request))


def register(request):
    if request.method == 'GET':
        return render_to_response('register.html', context_instance=RequestContext(request))
    if request.method == 'POST':
        phone = request.POST.get('phone')
        verify = request.POST.get('verify')
        password = request.POST.get('password')
        name = request.POST.get('name')
        work_num = request.POST.get('work_num')
        area = request.POST.get('area')
        if phone and verify and password and name and work_num and area:
            phone = int(phone)
            phone_verify = PhoneVerify.objects.filter(phone=phone)
            if phone_verify.count() == 0:
                return render_to_response('register.html', {'fault0': 'T'}, context_instance=RequestContext(request))
            else:
                area_admin = HomeAdmin()
                area_admin.phone = phone
                password = hashlib.md5(password).hexdigest()
                area_admin.password = password
                area_admin.name = name
                area_admin.work_num = work_num
                area_admin.area = area
                area_admin.save()
                request.session['user'] = phone
                return HttpResponseRedirect('login_in')
        else:
            return render_to_response('register.html', context_instance=RequestContext(request))

def forget_password(request):
    if request.method == 'GET':
        return render_to_response('forget_password.html')


def operate_new(request):
    if request.method == 'GET':
        items = [1, 2, 3, 4, 5, 6]
        return render_to_response('admin_area/operate_new.html', {'items': items})


def operate_get(request):
    if request.method == 'GET':
        items = [1, 2, 3, 4, 5, 6]
        return render_to_response('admin_area/operate_get.html', {'items': items})


def operate_finish(request):
    if request.method == 'GET':
        items = [1, 2, 3, 4, 5, 6]
        return render_to_response('admin_area/operate_finish.html', {'items': items})


def operate_cancel(request):
    if request.method == 'GET':
        items = [1, 2, 3, 4, 5, 6]
        return render_to_response('admin_area/operate_cancel.html', {'items': items})


def user_mes(request):
    if request.method == 'GET':
        return render_to_response('admin_area/user_mes.html')


def about(request):
    if request.method == 'GET':
        return render_to_response('admin_area/about.html')