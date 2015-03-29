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
import time

# Create your views here.

cities = [{'city_num': 510100, 'area_name': '四川省成都市'},
          {'city_num': 510181, 'area_name': '四川省都江堰市'},
          {'city_num': 510182, 'area_name': '四川省彭州市'},
          {'city_num': 510183, 'area_name': '四川省邛崃市'},
          {'city_num': 510184, 'area_name': '四川省崇州市'},
          {'city_num': 510300, 'area_name': '四川省自贡市'},
          {'city_num': 510400, 'area_name': '四川省攀枝花市'},
          {'city_num': 510500, 'area_name': '四川省泸州市'},
          {'city_num': 510600, 'area_name': '四川省德阳市'},
          {'city_num': 510681, 'area_name': '四川省广汉市'},
          {'city_num': 510682, 'area_name': '四川省什邡市'},
          {'city_num': 510683, 'area_name': '四川省绵竹市'},
          {'city_num': 510700, 'area_name': '四川省绵阳市'},
          {'city_num': 510800, 'area_name': '四川省广元市'},
          {'city_num': 510900, 'area_name': '四川省遂宁市'},
          {'city_num': 511000, 'area_name': '四川省内江市'},
          {'city_num': 511100, 'area_name': '四川省乐山市'},
          {'city_num': 511181, 'area_name': '四川省峨眉山市'},
          {'city_num': 511300, 'area_name': '四川省南充市'},
          {'city_num': 511381, 'area_name': '四川省阆中市'},
          {'city_num': 511500, 'area_name': '四川省宜宾市'},
          {'city_num': 511600, 'area_name': '四川省广安市'},
          {'city_num': 511681, 'area_name': '四川省华蓥市'},
          {'city_num': 513001, 'area_name': '四川省达川市'},
          {'city_num': 513002, 'area_name': '四川省万源市'},
          {'city_num': 513101, 'area_name': '四川省雅安市'},
          {'city_num': 513401, 'area_name': '四川省西昌市'},
          {'city_num': 513701, 'area_name': '四川省巴中市'},
          {'city_num': 513901, 'area_name': '四川省资阳市'},
          {'city_num': 513902, 'area_name': '四川省简阳市'},
          {'city_num': 513200, 'area_name': '四川省阿坝藏族羌族自治州'},
          {'city_num': 513300, 'area_name': '四川省甘孜藏族自治州'},
          {'city_num': 513400, 'area_name': '四川省凉山彝族自治州'}]


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
        area_num = request.GET.get('area')
        status = request.GET.get('type')
        areas_all = Block.objects.all()
        #查询首页
        if not page_num:
            #查看某段时间的预约
            if date_start and date_end and area_num and status:
                area = Block.objects.get(city_num=area_num)
                result = find_sometime_appointment(1, date_start, date_end, int(status), area)
                appointments = result['appointments']
                count = result['count']
                return render_to_response('admin_all/find_appointment.html',
                                          {'items': appointments,
                                           'count': count,
                                           'flag': 'T',
                                           'date_start': date_start,
                                           'date_end': date_end,
                                           'status': status,
                                           'area': area,
                                           'areas': areas_all}, context_instance=RequestContext(request))
            else:
                return render_to_response('admin_all/find_appointment.html',
                                          {'areas': areas_all})

        #查询某一页
        else:
            #查询某段时间预约的某一页
            if date_start and date_end and area_num and status:
                area = Block.objects.get(city_num=area_num)
                result = find_sometime_appointment(page_num, date_start, date_end, int(status), area)
                appointments = result['appointments']
                count = result['count']
                print "OK"
                return render_to_response('admin_all/find_appointment.html',
                                          {'items': appointments,
                                           'count': count,
                                           'flag': 'T',
                                           'date_start': date_start,
                                           'date_end': date_end,
                                           'status': status,
                                           'area': area,
                                           'areas': areas_all}, context_instance=RequestContext(request))
            else:
                return render_to_response('admin_all/find_appointment.html', {'areas': areas_all})


def find_sometime_appointment(page_num, date_start, date_end, status, area):
    end_time = time.strptime(date_end, "%Y-%m-%d")
    start_time = time.strptime(date_start, "%Y-%m-%d")
    end_time = datetime.datetime(*end_time[:6])
    start_time = datetime.datetime(*start_time[:6])
    if status == 0:
        appointments = Appointment.objects.order_by('-id').filter(create_time__lte=end_time,
                                                                  create_time__gte=start_time,
                                                                  area=area)
    else:
        appointments = Appointment.objects.order_by('-id').filter(create_time__lte=end_time,
                                                                  create_time__gte=start_time,
                                                                  status=status,
                                                                  area=area)
    count = appointments.count()
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
                old_area = Block.objects.get(id=item.old_area_id)
                new_area = Block.objects.get(id=item.new_area_id)
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
                new_area = Block.objects.get(id=c_a_apply.new_area_id)
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
            return render_to_response('admin_all/edit_area_detail.html',
                                      {'areas': cities})
        else:
            area = Block.objects.get(id=area_id)
            return render_to_response('admin_all/edit_area_detail.html', {'area': area})
    if request.method == 'POST':
        area_id = request.POST.get('area_id')
        area_num = request.POST.get('area_num')
        area_tel = request.POST.get('area_tel')
        area_address = request.POST.get('address')
        area_have = Block.objects.filter(city_num=area_num)
        if area_have.count() > 0:
            if not area_id:
                return HttpResponse(json.dumps('F'), content_type="application/json")

        if not area_id:
            new_area = Block()
            print "OK"
            new_area.city_num = area_num
            for item in cities:
                if item['city_num'] == int(area_num):
                    new_area.area_name = item['area_name']
                    break

            new_area.area_tel = area_tel
            new_area.area_address = area_address
            new_area.save()
            return HttpResponse(json.dumps('T'), content_type="application/json")
        else:
            area = Block.objects.get(id=area_id)
            area.area_tel = area_tel
            area.area_address = area_address
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
