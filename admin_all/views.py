# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response
from django.core.context_processors import csrf
from django.views.decorators.csrf import ensure_csrf_cookie
from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.template import RequestContext
from django.core.paginator import Paginator
from django.core.paginator import PageNotAnInteger
from django.core.paginator import EmptyPage
from HomeApi.models import *
from HomeApi.method import *
import json
import simplejson
import hashlib
import datetime

# Create your views here.


def login_in(request):
    if request.method == 'GET':
        return render_to_response('master_login.html', context_instance=RequestContext(request))
    if request.method == 'POST':
        context = {}
        context.update(csrf(request))
        username = request.POST.get('username')
        password = request.POST.get('password')
        if not username and not password:
            return render_to_response('master_login.html', context_instance=RequestContext(request))
        users = HomeAdmin.objects.filter(username=username, type=2)
        if users.count() == 0:
            return render_to_response('master_login.html', {'fault': 'T'}, context_instance=RequestContext(request))
        else:
            if not users[0].verify:
                return render_to_response('master_login.html', {'fault': 'T'}, context_instance=RequestContext(request))
            else:
                if not users[0].check_password(password):
                    return render_to_response('master_login.html', {'fault': 'T'},
                                              context_instance=RequestContext(request))
                else:
                    request.session['a_username'] = username
                    return HttpResponseRedirect('find_appointment')


def find_appointment(request):
    if not request.session.get('a_username'):
        return HttpResponseRedirect('login_in')
    if request.method == 'GET':
        page_num = request.GET.get('page')
        date_start = request.GET.get('start_date')
        date_end = request.GET.get('end_date')
        area = request.GET.get('area')
        type = request.GET.get('type')

        #检查是否是查询某段时间的操作
        if date_start and date_end and area and type:
            request.session['a_date_start'] = date_start
            request.session['a_date_end'] = date_end
            request.session['area'] = area
            request.session['type'] = type
        #查询首页
        if not page_num:
            #查看某段时间的预约
            if date_start and date_end and area and type:
                if type == '0':
                    all_appointments = Appointment.objects.order_by('-id').all()
                else:
                    type = int(type)
                    all_appointments = Appointment.objects.order_by('-id').filter(status=type)

                result = find_sometime_appointment(1, date_start, date_end, all_appointments)
                appointments = result['appointments']
                count = result['count']
                return render_to_response('admin_all/find_appointment.html',
                                          {'items': appointments,
                                           'count': count,
                                           'flag': 'T',
                                           'date_start': date_start,
                                           'date_end': date_end}, context_instance=RequestContext(request))
            else:
                return render_to_response('admin_all/find_appointment.html')

        #查询某一页
        else:
            #查询某段时间预约的某一页
            if request.session.get('a_date_start') and request.session.get('a_date_end') and request.session.get('type') and request.session['area']:
                date_start = request.session['a_date_start']
                date_end = request.session['a_date_end']
                type = request.session['type']
                area = request.session['area']
                if type == '0':
                    all_appointments = Appointment.objects.order_by('-id').all()
                else:
                    type = int(type)
                    all_appointments = Appointment.objects.order_by('-id').filter(status=type)

                result = find_sometime_appointment(page_num, date_start, date_end, all_appointments)
                appointments = result['appointments']
                count = result['count']
                return render_to_response('admin_all/find_appointment.html',
                                          {'items': appointments,
                                           'count': count,
                                           'flag': 'T',
                                           'date_start': date_start,
                                           'date_end': date_end}, context_instance=RequestContext(request))
            else:
                return render_to_response('admin_all/find_appointment.html')


def find_sometime_appointment(page_num, date_start, date_end, all_appointments):
    appointments = []
    if all_appointments.count() > 0:
        for item in all_appointments:
            it_date = str(item.create_time)[0:10]
            date_start = str(date_start)
            date_end = str(date_end)
            if it_date >= date_start and it_date <= date_end:
                appointments.append(item)
            else:
                continue
    count = len(appointments)
    paginator = Paginator(appointments, 1)
    try:
        appointments = paginator.page(page_num)
    except PageNotAnInteger:
        appointments = paginator.page(1)
    except EmptyPage:
        appointments = paginator.page(paginator.num_pages)
    except:
        pass

    return {'appointments': appointments, 'count': count}


def manage_admin(request):
    if not request.session.get('a_username'):
        return HttpResponseRedirect('login_in')

    if request.method == 'GET':
        users = HomeAdmin.objects.order_by('-id').filter(type=1)
        return render_to_response('admin_all/manage_admin.html', {'items': users},
                                  context_instance=RequestContext(request))


def delete_admin(request):
    if not request.session.get('a_username'):
        return HttpResponseRedirect('login_in')

    if request.method == 'POST':
        context = {}
        context.update(csrf(request))
        admins = request.POST.get('admins[]')
        print admins
        # for item in admins:
        #     print item
        #     user = HomeAdmin.objects.get(username=item, type=1)
        #     print 'OK'
        #     user.delete()

        return HttpResponse(json.dumps('T'))



def manage_apply(request):
    if request.method == 'GET':
        items = range(0, 10)
        return render_to_response('admin_all/manage_apply.html', {'items': items})


def about(request):
    if request.method == 'GET':
        return render_to_response('admin_all/about.html')