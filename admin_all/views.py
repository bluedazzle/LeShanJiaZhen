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
        area_name = request.GET.get('area')
        status = request.GET.get('type')

        #检查是否是查询某段时间的操作
        if date_start and date_end and area_name and status:
            request.session['a_date_start'] = date_start
            request.session['a_date_end'] = date_end
            request.session['area'] = area_name
            request.session['status'] = status
        #查询首页
        if not page_num:
            #查看某段时间的预约
            if date_start and date_end and area_name and status:
                area = Block.objects.get(area_name=area_name)
                if status == '0':
                    all_appointments = Appointment.objects.order_by('-id').filter(area=area)
                else:
                    status = int(status)
                    all_appointments = Appointment.objects.order_by('-id').filter(status=status, area=area)

                result = find_sometime_appointment(1, date_start, date_end, all_appointments)
                appointments = result['appointments']
                count = result['count']
                return render_to_response('admin_all/find_appointment.html',
                                          {'items': appointments,
                                           'count': count,
                                           'flag': 'T',
                                           'date_start': date_start,
                                           'date_end': date_end,
                                           'status': status,
                                           'area': area_name}, context_instance=RequestContext(request))
            else:
                return render_to_response('admin_all/find_appointment.html')

        #查询某一页
        else:
            #查询某段时间预约的某一页
            if request.session.get('a_date_start') and request.session.get('a_date_end') and request.session.get('status') and request.session['area']:
                date_start = request.session['a_date_start']
                date_end = request.session['a_date_end']
                status = request.session['status']
                area_name = request.session['area']
                area = Block.objects.get(area_name=area_name)
                if status == 0:
                    all_appointments = Appointment.objects.order_by('-id').filter(area=area)
                else:
                    status = int(status)
                    all_appointments = Appointment.objects.order_by('-id').filter(status=status, area=area)

                result = find_sometime_appointment(page_num, date_start, date_end, all_appointments)
                appointments = result['appointments']
                count = result['count']
                return render_to_response('admin_all/find_appointment.html',
                                          {'items': appointments,
                                           'count': count,
                                           'flag': 'T',
                                           'date_start': date_start,
                                           'date_end': date_end,
                                           'status': status,
                                           'area': area_name}, context_instance=RequestContext(request))
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
    paginator = Paginator(appointments, 15)
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


def edit_admin(request):
    if not request.session.get('a_username'):
        return HttpResponseRedirect('login_in')
    if request.method == 'GET':
        area_admin_id = request.GET.get('admin_id')
        area_admin = HomeAdmin.objects.filter(id=area_admin_id, type=1)
        if area_admin.count() == 0:
            return HttpResponseRedirect('manage_admin')

        return render_to_response('admin_all/edit_admin.html',
                                  {'admin': area_admin[0]},
                                  context_instance=RequestContext(request))
    if request.method == 'POST':
        context = {}
        context.update(csrf(request))
        area_admin_id = request.POST.get('admin_id')
        manage_game = request.POST.get('manage_game')
        manage_check_vip = request.POST.get('manage_check_vip')
        manage_send_message = request.POST.get('manage_send_message')
        manage_coupon = request.POST.get('manage_coupon')
        area_admin = HomeAdmin.objects.get(id=area_admin_id)
        if not area_admin:
            return HttpResponseRedirect('manage_admin')

        if manage_game == 'True':
            area_admin.manage_game = True
        else:
            area_admin.manage_game = False

        if manage_check_vip == 'True':
            area_admin.manage_check_vip = True
        else:
            area_admin.manage_check_vip = False

        if manage_send_message == 'True':
            area_admin.manage_send_message = True
        else:
            area_admin.manage_send_message = False

        if manage_coupon == 'True':
            area_admin.manage_coupon = True
        else:
            area_admin.manage_coupon = False

        area_admin.save()
        return HttpResponseRedirect('manage_admin')

def delete_admin(request):
    if not request.session.get('a_username'):
        return HttpResponseRedirect('login_in')
    if request.method == 'GET':
        area_admin_id = request.GET.get('admin_id')
        area_admin = HomeAdmin.objects.get(id=area_admin_id, type=1)
        try:
            area_admin.delete()

        except:
            pass
        return HttpResponseRedirect('manage_admin')


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


def manage_area(request):
    if not request.session.get('a_username'):
        return HttpResponseRedirect('login_in')
    if request.method == 'GET':
        areas = Block.objects.all()
        return render_to_response('admin_all/manage_area.html', {'areas': areas})


def edit_area(request):
    if not request.session.get('a_username'):
        return HttpResponseRedirect('login_in')
    if request.method == 'GET':
        area_id = request.GET.get('area_id')
        if not area_id:
            return render_to_response('admin_all/edit_area_detail.html')
        else:
            area = Block.objects.get(id=area_id)
            return render_to_response('admin_all/edit_area_detail.html', {'item': area})
    if request.method == 'POST':
        area_id = request.POST.get('area_id')
        area_name = request.POST.get('area_name')
        area_tel = request.POST.get('area_tel')
        area_address = request.POST.get('address')
        area_have = Block.objects.filter(area_name=area_name)
        if area_have.count() > 0:
            return HttpResponse(json.dumps('F'), content_type="application/json")

        lat = "43.32515"
        lng = "100.33242"
        if not area_id:
            new_area = Block()
            print "OK"
            new_area.area_id = -1
            new_area.area_name = area_name
            new_area.area_tel = area_tel
            new_area.area_address = area_address
            new_area.lat = lat
            new_area.lng = lng
            new_area.save()
            new_area.area_id = new_area.id
            new_area.save()
            return HttpResponse(json.dumps('T'), content_type="application/json")
        else:
            area = Block.objects.get(id=area_id)
            area.area_name = area_name
            area.area_tel = area_tel
            area.area_address = area_address
            area.lat = lat
            area.lng = lng
            area.save()
            return HttpResponse(json.dumps('T'), content_type="application/json")


def delete_area(request):
    if not request.session.get('a_username'):
        return HttpResponseRedirect('login_in')
    if request.method == 'GET':
        area_id = request.GET.get('area_id')
        if area_id:
            area = Block.objects.get(id=area_id)
            area.delete()
            return HttpResponseRedirect('manage_area')


def manage_calendar(request):
    if not request.session.get('a_username'):
        return HttpResponseRedirect('login_in')
    if request.method == 'GET':
        return render_to_response('admin_all/manage_calendar.html')
