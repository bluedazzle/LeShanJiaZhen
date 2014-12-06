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
                area_admin.save()
                if area == '1':
                    area_fi = Block.objects.get(area_id=1)
                    area_admin.area = area_fi
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
        #     for item in appointment:
        #         appointments.append(item)
        #
        count = appointments.count()
        paginator = Paginator(appointments, 10)
        try:
            request.session['new_appointment_id'] = appointments[0].id
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
            if not appointments[0].id == request.session['new_appointment_id']:
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
                   'notice_id': notice_id}
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
        #     for item in appointment:
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
                it_date = str(item.create_time)[0:10]
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
            it_date = str(item.create_time)[0:10]
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
        if applications.count() > 0:
            return render_to_response('admin_area/user_mes.html', {'user': user, 'have_apply': 'T'})

        return render_to_response('admin_area/user_mes.html', {'user': user})


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
        if password and area:
            user = HomeAdmin.objects.get(username=username)
            if not user.check_password(password):
                return HttpResponse(json.dumps('F'), content_type="application/json")

            applications = Application.objects.filter(apply_user=user)
            if applications.count() > 0:
                return HttpResponse(json.dumps('F1'), content_type="application/json")

            if area == '0':
                area_now = Block.objects.get(area_id=1)
            else:
                area_now = Block.objects.get(area_id=2)
            if area_now == user.area:
                return HttpResponse(json.dumps('F2'), content_type="application/json")

            new_application = Application()
            new_application.old_area_id = user.area.area_id
            new_application.new_area_id = area_now.area_id
            new_application.apply_user = user
            new_application.save()
            return HttpResponse(json.dumps('T'), content_type="application/json")

        return HttpResponse(json.dumps('F3'), content_type="application/json")



def notice(request):
    if not request.session.get('username'):
        return HttpResponseRedirect('login_in')
    if request.method == 'GET':
        notices = Notice.objects.order_by('-id').all()
        notice = []
        if notices.count() > 0:
            request.session['notice_id'] = notices[0].id
            for item in notices:
                notice.append(item)
                if len(notice) >= 5:
                    break

        return render_to_response('admin_area/notice.html', {'items': notice})


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
        appointment = request.POST.get('appointment')
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