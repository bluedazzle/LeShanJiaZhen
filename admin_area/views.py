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
BASE = os.path.dirname(os.path.dirname(__file__))


def login_in(request):
    if request.method == 'GET':
        return render_to_response('login_in.html', context_instance=RequestContext(request))
    if request.method == 'POST':
        context = {}
        context.update(csrf(request))
        username = request.POST.get('username')
        password = request.POST.get('password')
        if not username and not password:
            return render_to_response('login_in.html', context_instance=RequestContext(request))
        users = HomeAdmin.objects.filter(username=username)
        if users.count() == 0:
            return render_to_response('login_in.html', {'fault': 'T'}, context_instance=RequestContext(request))
        else:
            if not users[0].verify:
                return render_to_response('login_in.html', {'fault': 'T'}, context_instance=RequestContext(request))
            else:
                if not users[0].check_password(password):
                    return render_to_response('login_in.html', {'fault': 'T'}, context_instance=RequestContext(request))
                else:
                    request.session['username'] = username
                    return HttpResponseRedirect('notice')


def register(request):
    if request.method == 'GET':
        areas = Block.objects.all()
        return render_to_response('register.html',
                                  {'areas': areas},
                                  context_instance=RequestContext(request))
    if request.method == 'POST':
        phone = request.POST.get('phone')
        verify = request.POST.get('verify')
        password = request.POST.get('password')
        name = request.POST.get('name')
        work_num = request.POST.get('work_num')
        area = request.POST.get('area')
        if phone and verify and password and name and work_num and area:
            phone = int(phone)
            user = HomeAdmin.objects.filter(username=phone)
            if user.count() > 0:
                return render_to_response('register.html', {'fault0': 'T'}, context_instance=RequestContext(request))
            verify_phone = PhoneVerify.objects.filter(phone=phone, verify=verify)
            if verify_phone.count() == 0:
                return render_to_response('register.html', {'fault1': 'T'}, context_instance=RequestContext(request))
            else:
                verify_phone[0].delete()
                area_admin = HomeAdmin()
                area_admin.username = phone
                password = hashlib.md5(password).hexdigest()
                area_admin.password = password
                area_admin.nick = name
                area_admin.work_num = work_num
                time_now = datetime.datetime.now()
                area_admin.log_time = time_now
                area_admin.type = 1
                area_block = Block.objects.get(area_name=area)
                area_admin.area = area_block
                area_admin.save()
                return HttpResponseRedirect('login_in')
        else:
            return render_to_response('register.html', context_instance=RequestContext(request))


def phone_verify(request):
    if request.method == 'POST':
        context = {}
        context.update(csrf(request))
        phone = request.POST.get('phone')
        merchant_have = HomeAdmin.objects.filter(username=phone)
        if merchant_have.count() > 0:
            return HttpResponse(json.dumps("false"), content_type="application/json")
        req = createverfiycode(phone)
        print req
        return HttpResponse(json.dumps("true"), content_type="application/json")
    raise Http404


def f_phone_verify(request):
    if request.method == 'POST':
        context = {}
        context.update(csrf(request))
        phone = request.POST.get('phone')
        admin_have = HomeAdmin.objects.filter(username=phone, type=1)
        if admin_have.count() == 0:
            return HttpResponse(json.dumps("false"), content_type="application/json")
        req = createverfiycode(phone)
        print req
        return HttpResponse(json.dumps("true"), content_type="application/json")
    raise Http404


def forget_password(request):
    if request.method == 'GET':
        return render_to_response('forget_password.html', context_instance=RequestContext(request))
    if request.method == 'POST':
        context = {}
        context.update(csrf(request))
        phone = request.POST.get('phone')
        verify = request.POST.get('verify')
        password = request.POST.get('password')
        password_again = request.POST.get('password_again')
        if phone and verify and password and password_again:
            if not password == password_again:
                return render_to_response('forget_password.html', {'fault': 'T'},
                                          context_instance=RequestContext(request))
            else:
                print "OK"
                verify_phone = PhoneVerify.objects.filter(phone=phone, verify=verify)
                if verify_phone.count() > 0:
                    user = HomeAdmin.objects.get(username=phone)
                    password = hashlib.md5(password).hexdigest()
                    user.password = password
                    user.save()
                    return HttpResponseRedirect('login_in')
                else:
                    return render_to_response('forget_password.html', {'fault': 'T'},
                                              context_instance=RequestContext(request))
        else:
            return render_to_response('forget_password.html', context_instance=RequestContext(request))


def operate_new(request):
    if request.method == 'GET':
        if not request.session.get('username'):
            return HttpResponseRedirect('login_in')
        username = request.session['username']
        user = HomeAdmin.objects.get(username=username)
        appointments = Appointment.objects.order_by('-id').filter(area=user.area, status=1)
        # appointments = []
        # for i in range(0, 10):
        #     for item in appointments:
        #         appointments.append(item)
        #
        count = appointments.count()
        if count == 0:
            request.session['new_appointment_id'] = -1
        else:
            request.session['new_appointment_id'] = appointments[0].id
        paginator = Paginator(appointments, 10)
        try:
            page_num = request.GET.get('page')
            appointments = paginator.page(page_num)
        except PageNotAnInteger:
            appointments = paginator.page(1)
        except EmptyPage:
            appointments = paginator.page(paginator.num_pages)
        except:
            pass
        return render_to_response('admin_area/operate_new.html', {'items': appointments, 'count': count})


def get_new_appointment(request):
    if not request.session.get('username'):
        return HttpResponseRedirect('login_in')
    else:
        user = request.session['username']
        area_admin = HomeAdmin.objects.get(username=user)
        # area_admin.last_login = datetime.datetime.now()
        # area_admin.save()
        appointments = Appointment.objects.order_by('-id').filter(area=area_admin.area, status=1)
        if appointments.count() == 0:
            return HttpResponse(json.dumps('F'), content_type="application/json")
        else:
            if not request.session.get('new_appointment_id'):
                return HttpResponse(json.dumps('T'), content_type="application/json")
            if appointments[0].id > request.session['new_appointment_id']:
                return HttpResponse(json.dumps('T'), content_type="application/json")
            else:
                return HttpResponse(json.dumps('F'), content_type="application/json")


def get_new_appointment_count(request):
    if not request.session.get('username'):
        return HttpResponseRedirect('login_in')
    else:
        user = request.session['username']
        area_admin = HomeAdmin.objects.get(username=user)
        appointments = Appointment.objects.filter(area=area_admin.area, status=1)
        count_num = appointments.count()
        notices = Notice.objects.order_by("-id").all()
        notice_id = 'F'
        if notices.count() > 0:
            if request.session.get('notice_id'):
                if request.session['notice_id'] != notices[0].id:
                    notice_id = 'T'

        content = {'new_appointment': count_num,
                   'notice_id': notice_id,
                   'n_area': area_admin.area.area_name}
        return HttpResponse(json.dumps(content))


def operate_get(request):
    if request.method == 'GET':
        if not request.session['username']:
            return HttpResponseRedirect('login_in')
        username = request.session['username']
        user = HomeAdmin.objects.get(username=username)
        appointments = Appointment.objects.order_by('-id').filter(area=user.area, status=2)
        count = appointments.count()
        # appointments = []
        # for i in range(0, 10):
        #     for item in appointments:
        #         appointments.append(item)

        paginator = Paginator(appointments, 10)
        try:
            page_num = request.GET.get('page')
            appointments = paginator.page(page_num)
        except PageNotAnInteger:
            appointments = paginator.page(1)
        except EmptyPage:
            appointments = paginator.page(paginator.num_pages)
        except:
            pass
        return render_to_response('admin_area/operate_get.html', {'items': appointments, 'count': count})


def operate_finish(request):
    if not request.session.get('username'):
            return HttpResponseRedirect('login_in')

    if request.method == 'GET':
        username = request.session['username']
        user = HomeAdmin.objects.get(username=username)
        all_appointments = Appointment.objects.order_by('-id').filter(area=user.area, status=3)
        page_num = request.GET.get('page')
        date_start = request.GET.get('date_start')
        date_end = request.GET.get('date_end')
        #检查是否是查询某段时间的操作
        if date_start and date_end:
            request.session['f_date_start'] = date_start
            request.session['f_date_end'] = date_end
        #查询首页
        if not page_num:
            #查看当天的预约
            if not date_start and not date_end:
                if request.session.get('f_date_start') and request.session.get('f_date_end'):
                    del request.session['f_date_start']
                    del request.session['f_date_end']
                result = find_now_appointment(1, all_appointments)
                appointments = result['appointments']
                count = result['count']
                return render_to_response('admin_area/operate_finish.html',
                                          {'items': appointments,
                                           'count': count,
                                           'flag0': 'T'}, context_instance=RequestContext(request))
            #查看某段时间的预约
            else:
                result = find_sometime_appointment(1, date_start, date_end, all_appointments)
                appointments = result['appointments']
                count = result['count']
                return render_to_response('admin_area/operate_finish.html',
                                          {'items': appointments,
                                           'count': count,
                                           'flag': 'T',
                                           'date_start': date_start,
                                           'date_end': date_end}, context_instance=RequestContext(request))
        #查询某一页
        else:
            #查询某段时间预约的某一页
            if request.session.get('f_date_start') and request.session.get('f_date_end'):
                date_start = request.session['f_date_start']
                date_end = request.session['f_date_end']
                result = find_sometime_appointment(page_num, date_start, date_end, all_appointments)
                appointments = result['appointments']
                count = result['count']
                return render_to_response('admin_area/operate_finish.html',
                                          {'items': appointments,
                                           'count': count,
                                           'flag': 'T',
                                           'date_start': date_start,
                                           'date_end': date_end}, context_instance=RequestContext(request))
            #查询当天预约的某一页
            else:
                result = find_now_appointment(page_num, all_appointments)
                appointments = result['appointments']
                count = result['count']
                return render_to_response('admin_area/operate_finish.html',
                                          {'items': appointments,
                                           'count': count,
                                           'flag0': 'T'}, context_instance=RequestContext(request))


def find_now_appointment(page_num, all_appointments):
    appointments = []
    if all_appointments.count() > 0:
            for item in all_appointments:
                now_date = str(datetime.datetime.now())[0:10]
                it_date = str(item.appoint_time)[0:10]
                if it_date == now_date:
                    appointments.append(item)
                else:
                    continue
    count = len(appointments)
    paginator = Paginator(appointments, 10)
    try:
        appointments = paginator.page(page_num)
    except PageNotAnInteger:
        appointments = paginator.page(1)
    except EmptyPage:
        appointments = paginator.page(paginator.num_pages)
    except:
        pass
    return {'appointments': appointments, 'count': count}


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
    paginator = Paginator(appointments, 10)
    try:
        appointments = paginator.page(page_num)
    except PageNotAnInteger:
        appointments = paginator.page(1)
    except EmptyPage:
        appointments = paginator.page(paginator.num_pages)
    except:
        pass

    return {'appointments': appointments, 'count': count}


def operate_cancel(request):
    if not request.session.get('username'):
            return HttpResponseRedirect('login_in')

    if request.method == 'GET':
        username = request.session['username']
        user = HomeAdmin.objects.get(username=username)
        all_appointments = Appointment.objects.order_by('-id').filter(area=user.area, status=4)
        page_num = request.GET.get('page')
        date_start = request.GET.get('date_start')
        date_end = request.GET.get('date_end')
        #检查是否是查询某段时间的操作
        if date_start and date_end:
            request.session['f_date_start'] = date_start
            request.session['f_date_end'] = date_end
        #查询首页
        if not page_num:
            #查看当天的预约
            if not date_start and not date_end:
                if request.session.get('f_date_start') and request.session.get('f_date_end'):
                    del request.session['f_date_start']
                    del request.session['f_date_end']
                result = find_now_appointment(1, all_appointments)
                appointments = result['appointments']
                count = result['count']
                return render_to_response('admin_area/operate_cancel.html',
                                          {'items': appointments,
                                           'count': count,
                                           'flag0': 'T'}, context_instance=RequestContext(request))
            #查看某段时间的预约
            else:
                result = find_sometime_appointment(1, date_start, date_end, all_appointments)
                appointments = result['appointments']
                count = result['count']
                return render_to_response('admin_area/operate_cancel.html',
                                          {'items': appointments,
                                           'count': count,
                                           'flag': 'T',
                                           'date_start': date_start,
                                           'date_end': date_end}, context_instance=RequestContext(request))
        #查询某一页
        else:
            #查询某段时间预约的某一页
            if request.session.get('f_date_start') and request.session.get('f_date_end'):
                date_start = request.session['f_date_start']
                date_end = request.session['f_date_end']
                result = find_sometime_appointment(page_num, date_start, date_end, all_appointments)
                appointments = result['appointments']
                count = result['count']
                return render_to_response('admin_area/operate_cancel.html',
                                          {'items': appointments,
                                           'count': count,
                                           'flag': 'T',
                                           'date_start': date_start,
                                           'date_end': date_end}, context_instance=RequestContext(request))
            #查询当天预约的某一页
            else:
                result = find_now_appointment(page_num, all_appointments)
                appointments = result['appointments']
                count = result['count']
                return render_to_response('admin_area/operate_cancel.html',
                                          {'items': appointments,
                                           'count': count,
                                           'flag0': 'T'}, context_instance=RequestContext(request))


def user_mes(request):
    if not request.session.get('username'):
        return HttpResponseRedirect('login_in')
    if request.method == 'GET':
        user = HomeAdmin.objects.get(username=request.session['username'])
        applications = Application.objects.filter(apply_user=user)
        areas = Block.objects.all()
        if applications.count() > 0:
            return render_to_response('admin_area/user_mes.html', {'user': user,
                                                                   'have_apply': 'T',
                                                                   'areas': areas})

        return render_to_response('admin_area/user_mes.html', {'user': user,
                                                               'areas': areas})


def change_password(request):
    if not request.session.get('username'):
        return HttpResponseRedirect('login_in')

    if request.method == 'POST':
        username = request.session['username']
        context = {}
        context.update(csrf(request))
        old_password = request.POST.get('old_password')
        new_password = request.POST.get('new_password')
        password_again = request.POST.get('password_again')
        if old_password and new_password and password_again:
            if old_password != new_password and new_password == password_again:
                user = HomeAdmin.objects.get(username=username)
                if user.check_password(old_password):
                    new_password = hashlib.md5(new_password).hexdigest()
                    user.password = new_password
                    user.save()
                    return HttpResponse(json.dumps('T'), content_type="application/json")
                else:
                    return HttpResponse(json.dumps('F'), content_type="application/json")

        return HttpResponse(json.dumps('F1'), content_type="application/json")


def change_area(request):
    if not request.session.get('username'):
        return HttpResponseRedirect('login_in')
    if request.method == 'POST':
        username = request.session['username']
        context = {}
        context.update(csrf(request))
        password = request.POST.get('password')
        area = request.POST.get('area')
        print "OK"
        if password and area:
            user = HomeAdmin.objects.get(username=username)
            if not user.check_password(password):
                return HttpResponse(json.dumps('F'), content_type="application/json")

            applications = Application.objects.filter(apply_user=user)
            if applications.count() > 0:
                return HttpResponse(json.dumps('F1'), content_type="application/json")

            area_now = Block.objects.get(area_name=area)
            if area_now == user.area:
                return HttpResponse(json.dumps('F2'), content_type="application/json")

            new_application = Application()
            new_application.old_area_id = user.area.id
            new_application.new_area_id = area_now.id
            new_application.apply_user = user
            print "OK1"
            new_application.save()
            print "OK2"
            return HttpResponse(json.dumps('T'), content_type="application/json")

        return HttpResponse(json.dumps('F3'), content_type="application/json")


def notice(request):
    if not request.session.get('username'):
        return HttpResponseRedirect('login_in')
    if not request.session.get('username'):
            return HttpResponseRedirect('login_in')

    if request.method == 'GET':
        all_notice = Notice.objects.order_by('-id').all()
        if all_notice.count() == 0:
            return render_to_response('admin_area/notice.html')
        page_num = request.GET.get('page')
        date_start = request.GET.get('date_start')
        date_end = request.GET.get('date_end')
        #检查是否是查询某段时间的操作
        if date_start and date_end:
            request.session['notice_date_start'] = date_start
            request.session['notice_date_end'] = date_end
        #查询首页
        if not page_num:
            #查看某段时间的公告
            if date_start and date_end:
                result = find_sometime_notices(1, date_start, date_end, all_notice)
                all_notices = result['notices']
                count = result['count']
                return render_to_response('admin_area/notice.html',
                                          {'items': all_notices,
                                           'count': count,
                                           'flag': 'T',
                                           'date_start': date_start,
                                           'date_end': date_end}, context_instance=RequestContext(request))
            #查看所有公告
            else:
                if request.session.get('notice_date_start') and request.session.get('notice_date_end'):
                    del request.session['notice_date_start']
                    del request.session['notice_date_end']
                request.session['notice_id'] = all_notice[0].id
                result = find_all_notices(1, all_notice)
                all_notices = result['notices']
                count = result['count']
                return render_to_response('admin_area/notice.html',
                                          {'items': all_notices,
                                           'count': count,
                                           'flag0': 'T'}, context_instance=RequestContext(request))
        #查询某一页
        else:
            #查询某段时间公告的某一页
            if request.session.get('notice_date_start') and request.session.get('notice_date_end'):
                date_start = request.session['notice_date_start']
                date_end = request.session['notice_date_end']
                result = find_sometime_notices(page_num, date_start, date_end, all_notice)
                all_notices = result['notices']
                count = result['count']
                return render_to_response('admin_area/notice.html',
                                          {'items': all_notices,
                                           'count': count,
                                           'flag': 'T',
                                           'date_start': date_start,
                                           'date_end': date_end}, context_instance=RequestContext(request))
            #查询所有公告的某一页
            else:
                result = find_all_notices(page_num, all_notice)
                all_notices = result['notices']
                count = result['count']
                return render_to_response('admin_area/notice.html',
                                          {'items': all_notices,
                                           'count': count,
                                           'flag0': 'T'}, context_instance=RequestContext(request))


def find_all_notices(page_num, all_notices):
    notices = []
    if all_notices.count() > 0:
            for item in all_notices:
                notices.append(item)

    count = len(notices)
    paginator = Paginator(notices, 5)
    try:
        notices = paginator.page(page_num)
    except PageNotAnInteger:
        notices = paginator.page(1)
    except EmptyPage:
        notices = paginator.page(paginator.num_pages)
    except:
        pass
    return {'notices': notices, 'count': count}


def find_sometime_notices(page_num, date_start, date_end, all_notices):
    notices = []
    if all_notices.count() > 0:
        for item in all_notices:
            it_date = str(item.create_time)[0:10]
            date_start = str(date_start)
            date_end = str(date_end)
            if it_date >= date_start and it_date <= date_end:
                notices.append(item)
            else:
                continue
    count = len(notices)
    paginator = Paginator(notices, 5)
    try:
        notices = paginator.page(page_num)
    except PageNotAnInteger:
        notices = paginator.page(1)
    except EmptyPage:
        notices = paginator.page(paginator.num_pages)
    except:
        pass

    return {'notices': notices, 'count': count}


def find_appointment(request):
    if not request.session.get('username'):
        return HttpResponseRedirect('login_in')
    if request.method == 'GET':
        return render_to_response('admin_area/find_appointment.html', context_instance=RequestContext(request))

    if request.method == 'POST':
        username = request.session['username']
        context = {}
        context.update(csrf(request))
        phone = request.POST.get('phone')
        appointment = request.POST.get('appointments')
        if phone:
            user = HomeAdmin.objects.get(username=username)
            consumer = Consumer.objects.filter(phone=phone)
            if consumer.count() == 0:
                return render_to_response('admin_area/find_appointment.html',
                                          {'fault': 'T'},
                                          context_instance=RequestContext(request))
            consumer1 = consumer[0]
            appointments = Appointment.objects.order_by('-id').filter(consumer=consumer1, area=user.area)
            if appointments.count() == 0:
                return render_to_response('admin_area/find_appointment.html',
                                          {'fault': 'T'},
                                          context_instance=RequestContext(request))
            else:
                return render_to_response('admin_area/find_appointment.html',
                                          {'items': appointments},
                                          context_instance=RequestContext(request))
        if appointment:
            user = HomeAdmin.objects.get(username=username)
            appointments = Appointment.objects.order_by('-id').filter(area=user.area, id=appointment)
            if appointments.count() == 0:
                return render_to_response('admin_area/find_appointment.html',
                                          {'fault': 'T'},
                                          context_instance=RequestContext(request))
            else:
                return render_to_response('admin_area/find_appointment.html',
                                          {'items': appointments},
                                          context_instance=RequestContext(request))


def program_manage(request):
    if not request.session.get('username'):
        return HttpResponseRedirect('login_in')
    if request.method == 'GET':
        item_p_id = request.GET.get('item_p_id')
        user = HomeAdmin.objects.get(username=request.session['username'])
        programs = HomeItem_P.objects.order_by('sort_id').filter(area=user.area)
        if not item_p_id:
            return render_to_response('admin_area/program_manage/program_manage.html', {'programs': programs})
        else:
            item_p = HomeItem_P.objects.filter(id=item_p_id)
            if item_p.count() == 0:
                return render_to_response('admin_area/program_manage/program_manage.html', {'programs': programs})
            else:
                item_details = HomeItem.objects.order_by('sort_id').filter(parent_item=item_p)
                return render_to_response('admin_area/program_manage/program_manage.html', {'programs': programs,
                                                                             'item_details': item_details,
                                                                             'item_p': item_p[0],
                                                                             'flag0': 'T'})


def delete_program_detail(request):
    if not request.session.get('username'):
        return HttpResponseRedirect('login_in')
    if request.method == 'GET':
        item_id = request.GET.get('item_id')
        item_p_id = request.GET.get('item_p_id')
        item = HomeItem.objects.get(id=item_id)
        item.delete()
        return HttpResponseRedirect('program_manage?item_p_id='+item_p_id)


def advertisement_manage(request):
    if not request.session.get('username'):
        return HttpResponseRedirect('login_in')
    if request.method == 'GET':
        items = Advertisement.objects.all()
        return render_to_response('admin_area/advertisement_manage.html',
                                  {'items': items},
                                  context_instance=RequestContext(request))
    if request.method == 'POST':
        context = {}
        context.update(csrf(request))
        ad_file = request.FILES.get('file0', None)
        if ad_file == None:
            return HttpResponse('file not existing in the request')
        file_name = str(int(time.time())) + '.png'
        file_full_path = BASE + '/static/img/advertisement/' + file_name
        Image.open(ad_file).save(file_full_path)
        new_advertisement = Advertisement()
        new_advertisement.content = file_name
        new_advertisement.photo = 'http://115.29.138.80' + '/img/advertisement/'+file_name
        new_advertisement.save()
        return HttpResponseRedirect('advertisement_manage')


def delete_advertisement(request):
    if not request.session.get('username'):
        return HttpResponseRedirect('login_in')
    if request.method == 'GET':
        ad_id = request.GET.get('advertisement_id')
        advertisement = Advertisement.objects.get(id=ad_id)
        file_full_path = './static/img/advertisement/'+advertisement.content
        os.remove(file_full_path)
        advertisement.delete()
        return HttpResponseRedirect('advertisement_manage')


def edit_program_detail(request):
    if not request.session.get('username'):
        return HttpResponseRedirect('login_in')
    if request.method == 'GET':
        item_p_id = request.GET.get('item_p_id')
        item_id = request.GET.get('item_id')
        item_p = HomeItem_P.objects.get(id=item_p_id)
        if not item_id:
            return render_to_response('admin_area/program_manage/edit_program_detail.html',
                                      {'item_p': item_p},
                                      context_instance=RequestContext(request))
        item = HomeItem.objects.get(id=item_id)
        return render_to_response('admin_area/program_manage/edit_program_detail.html',
                                  {'item_p': item_p,
                                   'item': item},
                                  context_instance=RequestContext(request))
    if request.method == 'POST':
        item_name = request.POST.get('item_name')
        price = request.POST.get('price')
        content = request.POST.get('content')
        item_p_id = request.POST.get('item_p_id')
        item_sort_id = request.POST.get('sort_id')
        item_id = request.POST.get('item_id')
        if item_name and price and content and item_p_id:
            if item_id:
                item = HomeItem.objects.get(id=item_id)
                item.title = item_name
                item.price = price
                item.content = content
                item0 = HomeItem.objects.get(parent_item=item.parent_item, sort_id=item_sort_id)
                if not item0:
                    item.sort_id = item_sort_id
                else:
                    item0.sort_id = item.sort_id
                    item0.save()
                    item.sort_id = item_sort_id

                item.save()
                return HttpResponse(json.dumps('T'), content_type="application/json")

            item_p = HomeItem_P.objects.get(id=item_p_id)
            item_have = HomeItem.objects.filter(parent_item=item_p, sort_id=item_sort_id)
            if item_have.count() != 0:
                return HttpResponse(json.dumps('F'), content_type="application/json")
            new_item = HomeItem()
            new_item.title = item_name
            new_item.price = price
            new_item.content = content
            new_item.parent_item = item_p
            new_item.sort_id = item_sort_id
            new_item.save()
            return HttpResponse(json.dumps('T'), content_type="application/json")
        else:
            return HttpResponse(json.dumps('F'), content_type="application/json")


def edit_program_p_detail(request):
    if not request.session.get('username'):
        return HttpResponseRedirect('login_in')
    if request.method == 'GET':
        item_id = request.GET.get('item_id')
        if item_id:
            item_p = HomeItem_P.objects.get(id=item_id)
            return render_to_response('admin_area/program_manage/edit_program_p_detail.html',
                                      {'item_p': item_p},
                                      context_instance=RequestContext(request))
        return render_to_response('admin_area/program_manage/edit_program_p_detail.html',
                                  context_instance=RequestContext(request))
    if request.method == 'POST':
        context = {}
        context.update(csrf(request))
        icon_file = request.FILES.get('icon_file')
        item_p_id = request.POST.get('item_p_id')
        item_sort_id = request.POST.get('sort_id')
        item_name = request.POST.get('item_name')
        user = HomeAdmin.objects.get(username=request.session['username'])
        i_id = 1
        item_p_have = HomeItem_P.objects.filter(sort_id=item_sort_id)

        if item_p_id:
            item_p = HomeItem_P.objects.get(id=item_p_id)
            if item_p.sort_id != int(item_sort_id):
                if item_p_have.count() > 0:
                    return render_to_response('admin_area/program_manage/edit_program_p_detail.html',
                                              {'sort_id_have': 'T',
                                              'item_p': item_p},
                                              context_instance=RequestContext(request))
            item_p.item_name = item_name
            item_p.sort_id = item_sort_id
            item_p.save()
            i_id = item_p.id
        else:
            new_item_p = HomeItem_P()
            new_item_p.item_name = item_name
            new_item_p.area = user.area
            new_item_p.sort_id = item_sort_id
            if item_p_have.count() > 0:
                return render_to_response('admin_area/program_manage/edit_program_p_detail.html',
                                          {'sort_id_have': 'T',
                                           'item_p': new_item_p}, context_instance=RequestContext(request))
            new_item_p.save()
            i_id = new_item_p.id
        if icon_file != None:
            print "OK"
            file_name = str(int(time.time())) + '.png'
            file_full_path = BASE + '/static/img/program_icons/' + file_name
            Image.open(icon_file).save(file_full_path)
            item_p = HomeItem_P.objects.get(id=i_id)
            item_p.icon = 'http://115.29.138.80'+'/img/program_icons/'+file_name
            item_p.save()

        return HttpResponseRedirect('program_manage')


def delete_program_p(request):
    if not request.session.get('username'):
        return HttpResponseRedirect('login_id')
    if request.method == 'GET':
        item_p_id = request.GET.get('item_id')
        item_p = HomeItem_P.objects.get(id=item_p_id)
        items = HomeItem.objects.filter(parent_item=item_p)
        if items.count() != 0:
            for item in items:
                item.delete()

        item_p.delete()
        return HttpResponseRedirect('program_manage')


def push_message(request):
    if not request.session.get('username'):
        return HttpResponseRedirect('login_in')
    if request.method == 'GET':
        return render_to_response('admin_area/push_message.html', context_instance=RequestContext(request))
    if request.method == 'POST':
        message = request.POST.get('mes_push')
        message = message.encode('utf-8')
        req = customedPush(message)
        if req:
            return HttpResponse(json.dumps('T'))
        else:
            return HttpResponse(json.dumps('F'))


def goods_manage(request):
    if not request.session.get('username'):
        return HttpResponseRedirect('login_in')
    if request.method == 'GET':
        goods_p = request.GET.get('goods_p')
        goods_o = request.GET.get('goods_o')
        goods_ps = Goods_P.objects.order_by('sort_id').all()
        if goods_p and not goods_o:
            Goods_p = Goods_P.objects.filter(id=goods_p)
            if Goods_p.count() == 0:
                return render_to_response('admin_area/goods_manage/goods_manage.html',
                                          {'goods_ps': goods_ps},
                                          content_type=RequestContext(request))

            goods_os = Goods_O.objects.order_by('sort_id').filter(parent_item=Goods_p)
            return render_to_response('admin_area/goods_manage/goods_manage_two.html',
                                      {'goods_os': goods_os},
                                      content_type=RequestContext(request))
        if goods_p and goods_o:
            Goods_o = Goods_O.objects.filter(id=goods_o)
            if Goods_o.count() == 0:
                return render_to_response('admin_area/goods_manage/goods_manage.html',
                                          {'goods_ps': goods_ps},
                                          content_type=RequestContext(request))

            goods = GoodsItem.objects.order_by('sort_id').filter(parent_item=Goods_o)
            return render_to_response('admin_area/goods_manage/goods_manage_three.html',
                                      {'goods': goods},
                                      content_type=RequestContext(request))

        return render_to_response('admin_area/goods_manage/goods_manage.html',
                                  {'goods_ps': goods_ps},
                                  content_type=RequestContext(request))


def add_goods_p(request):
    if not request.session.get('username'):
        return HttpResponseRedirect('login_in')
    if request.method == 'GET':
        return render_to_response('admin_area/goods_manage/edit_goods_p.html',
                                  content_type=RequestContext(request))


def coupon_manage(request):
    if not request.session.get('username'):
        return HttpResponseRedirect('login_in')
    if request.method == 'GET':
        return render_to_response('admin_area/coupon_manage.html', content_type=RequestContext(request))


def game_manage(request):
    if not request.session.get('username'):
        return HttpResponseRedirect('login_in')
    if request.method == 'GET':
        return render_to_response('admin_area/game_manage.html', content_type=RequestContext(request))


def vip_manage(request):
    if not request.session.get('username'):
        return HttpResponseRedirect('login_in')
    if request.method == 'GET':
        return render_to_response('admin_area/vip_manage.html', content_type=RequestContext(request))


def index(req):
    return render_to_response('index.html')

