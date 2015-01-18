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
import re
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
        area_id = request.GET.get('area')
        type = request.GET.get('type')

        #检查是否是查询某段时间的操作
        if date_start and date_end and area_id and type:
            request.session['a_date_start'] = date_start
            request.session['a_date_end'] = date_end
            request.session['area'] = area_id
            request.session['type'] = type
        #查询首页
        if not page_num:
            #查看某段时间的预约
            if date_start and date_end and area_id and type:
                area = Block.objects.get(area_id=area_id)
                if type == '0':
                    all_appointments = Appointment.objects.order_by('-id').filter(area=area)
                else:
                    type = int(type)
                    all_appointments = Appointment.objects.order_by('-id').filter(status=type, area=area)

                result = find_sometime_appointment(1, date_start, date_end, all_appointments)
                appointments = result['appointments']
                count = result['count']
                return render_to_response('admin_all/find_appointment.html',
                                          {'items': appointments,
                                           'count': count,
                                           'flag': 'T',
                                           'date_start': date_start,
                                           'date_end': date_end,
                                           'status': type,
                                           'area': area_id}, context_instance=RequestContext(request))
            else:
                return render_to_response('admin_all/find_appointment.html')

        #查询某一页
        else:
            #查询某段时间预约的某一页
            if request.session.get('a_date_start') and request.session.get('a_date_end') and request.session.get('type') and request.session['area']:
                date_start = request.session['a_date_start']
                date_end = request.session['a_date_end']
                type = request.session['type']
                area_id = request.session['area']
                area = Block.objects.get(area_id=area_id)
                if type == '0':
                    all_appointments = Appointment.objects.order_by('-id').filter(area=area)
                else:
                    type = int(type)
                    all_appointments = Appointment.objects.order_by('-id').filter(status=type, area=area)

                result = find_sometime_appointment(page_num, date_start, date_end, all_appointments)
                appointments = result['appointments']
                count = result['count']
                return render_to_response('admin_all/find_appointment.html',
                                          {'items': appointments,
                                           'count': count,
                                           'flag': 'T',
                                           'date_start': date_start,
                                           'date_end': date_end,
                                           'status': type,
                                           'area': area_id}, context_instance=RequestContext(request))
            else:
                return render_to_response('admin_all/find_appointment.html')


def find_sometime_appointment(page_num, date_start, date_end, all_appointments):
    appointments = []
    if all_appointments.count() > 0:
        for item in all_appointments:
            it_date = str(item.appoint_time)[0:10]
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
        users = HomeAdmin.objects.order_by('-id').filter(type=1, verify=True)
        return render_to_response('admin_all/manage_admin.html', {'items': users},
                                  context_instance=RequestContext(request))


def delete_admin(request):
    if not request.session.get('a_username'):
        return HttpResponseRedirect('login_in')

    if request.method == 'POST':
        context = {}
        context.update(csrf(request))
        admins = request.POST.get('admins')
        admin_list = re.findall(',(.*?),', admins, re.S)
        print admin_list
        for item in admin_list:
            print item
            user = HomeAdmin.objects.get(username=item, type=1)
            print "delete admin '"+user.username + "' OK"
            user.delete()

        return HttpResponse(json.dumps('T'))


def manage_apply(request):
    if not request.session.get('a_username'):
        return HttpResponseRedirect('login_in')

    if request.method == 'GET':
        applications = []
        apply_admins = HomeAdmin.objects.order_by('-id').filter(type=1, verify=False)
        apply_areas = Application.objects.order_by('-id').all()
        if apply_admins.count() > 0:
            for item in apply_admins:
                applications.append({'type': 'R', 'body': item})

        if apply_areas.count() > 0:
            for item in apply_areas:
                old_area = Block.objects.get(area_id=item.old_area_id)
                new_area = Block.objects.get(area_id=item.new_area_id)
                applications.append({'type': 'A', 'body': {'old_area': old_area,
                                                           'id': item.id,
                                                           'new_area': new_area,
                                                           'apply_time': item.apply_time,
                                                           'apply_user': item.apply_user}})

        return render_to_response('admin_all/manage_apply.html', {'items': applications})


def pass_application(request):
    if not request.session.get('a_username'):
        return HttpResponseRedirect('login_in')

    if request.method == 'POST':
        context = {}
        context.update(csrf(request))
        apply_num = request.POST.get('apply_num')
        print apply_num
        register_list = re.findall(',R(.*?),', apply_num, re.S)
        c_a_list = re.findall(',A(.*?),', apply_num, re.S)
        print register_list
        print c_a_list
        if register_list:
            for item in register_list:
                area_admin = HomeAdmin.objects.get(id=item, type=1)
                area_admin.verify = True
                area_admin.save()

        if c_a_list:
            for item in c_a_list:
                c_a_apply = Application.objects.get(id=item)
                new_area = Block.objects.get(area_id=c_a_apply.new_area_id)
                area_admin = c_a_apply.apply_user
                area_admin.area = new_area
                area_admin.save()
                c_a_apply.delete()
        return HttpResponse(json.dumps('T'))


def delete_application(request):
    if not request.session.get('a_username'):
        return HttpResponseRedirect('login_in')

    if request.method == 'POST':
        context = {}
        context.update(csrf(request))
        apply_num = request.POST.get('apply_num')
        print apply_num
        register_list = re.findall(',R(.*?),', apply_num, re.S)
        c_a_list = re.findall(',A(.*?),', apply_num, re.S)
        print register_list
        print c_a_list
        if register_list:
            for item in register_list:
                area_admin = HomeAdmin.objects.get(id=item, type=1)
                area_admin.delete()

        if c_a_list:
            for item in c_a_list:
                c_a_apply = Application.objects.get(id=item)
                c_a_apply.delete()
        return HttpResponse(json.dumps('T'))


def manage_notice(request):
    if not request.session.get('a_username'):
        return HttpResponseRedirect('login_in')

    if request.method == 'GET':
        notices = Notice.objects.all()
        return render_to_response('admin_all/manage_notice.html', {'items': notices})


def delete_notice(request):
    if not request.session.get('a_username'):
        return HttpResponseRedirect('login_in')

    if request.method == 'POST':
        context = {}
        context.update(csrf(request))
        notice_ids = request.POST.get('notice_ids')
        print notice_ids
        notice_id_list = re.findall(",(.*?),", notice_ids, re.S)
        print notice_id_list
        if notice_id_list:
            for item in notice_id_list:
                notice = Notice.objects.get(id=item)
                notice.delete()

            return HttpResponse(json.dumps('T'))
        else:
            return HttpResponse(json.dumps('F'))


def put_notice(request):
    if not request.session.get('a_username'):
        return HttpResponseRedirect('login_in')

    if request.method == 'POST':
        context = {}
        context.update(csrf(request))
        notice_text = request.POST.get('notice')
        new_notice = Notice()
        new_notice.content = notice_text
        new_notice.save()
        return HttpResponse(json.dumps('T'))
