# -*- coding: utf-8 -*-
from views import *
import xlwt
import sys


def get_appointment(request):
    if request.method == 'GET':
        if request.session.get('username'):
            id = request.GET.get('id')
            user = HomeAdmin.objects.get(username=request.session['username'])
            appointment = Appointment.objects.get(id=id, status=1)
            appointment.status = 2
            appointment.process_by = user
            appointment.save()
            return HttpResponseRedirect('operate_new')
        else:
            return HttpResponseRedirect('login_in')


def get_appointment_all(request):
    if request.method == 'GET':
        if request.session.get('username'):
            username = request.session['username']
            user = HomeAdmin.objects.get(username=username)
            appointments = Appointment.objects.filter(area=user.area, status=1)
            for item in appointments:
                item.status = 2
                item.process_by = user
                item.save()
            return HttpResponseRedirect('operate_new')
        else:
            return HttpResponseRedirect('login_in')


def cancel_appointment_n(request):
    if request.method == 'GET':
        if request.session.get('username'):
            id = request.GET.get('id')
            user = HomeAdmin.objects.get(username=request.session['username'])
            appointment = Appointment.objects.get(id=id, status=1)
            appointment.status = 4
            appointment.process_by = user
            appointment.save()
            return HttpResponseRedirect('operate_new')
        else:
            return HttpResponseRedirect('login_in')


def cancel_appointment_all_n(request):
    if request.method == 'GET':
        if request.session.get('username'):
            username = request.session['username']
            user = HomeAdmin.objects.get(username=username)
            appointments = Appointment.objects.filter(area=user.area, status=1)
            for item in appointments:
                item.status = 4
                item.area = user.area
                item.save()
            return HttpResponseRedirect('operate_new')
        else:
            return HttpResponseRedirect('login_in')


def cancel_appointment_g(request):
    if request.method == 'GET':
        if request.session.get('username'):
            id = request.GET.get('id')
            user = HomeAdmin.objects.get(username=request.session['username'])
            appointment = Appointment.objects.get(id=id, status=2)
            appointment.status = 4
            appointment.process_by = user
            appointment.save()
            return HttpResponseRedirect('operate_get')


def cancel_appointment_all_g(request):
    if request.method == 'GET':
        if request.session.get('username'):
            username = request.session['username']
            user = HomeAdmin.objects.get(username=username)
            appointments = Appointment.objects.filter(area=user.area, status=2)
            for item in appointments:
                item.status = 4
                item.process_by = user
                item.save()
            return HttpResponseRedirect('operate_get')
        else:
            return HttpResponseRedirect('login_in')


def finish_appointment(request):
    if request.method == 'GET':
        if request.session.get('username'):
            user = HomeAdmin.objects.get(username=request.session['username'])
            id = request.GET.get('id')
            appointment = Appointment.objects.get(id=id, status=2)
            appointment.status = 3
            appointment.process_by = user
            appointment.save()
            return HttpResponseRedirect('operate_get')


def finish_appointment_all(request):
    if request.method == 'GET':
        if request.session.get('username'):
            username = request.session['username']
            user = HomeAdmin.objects.get(username=username)
            appointments = Appointment.objects.get(area=user.area, status=2)
            for item in appointments:
                item.status = 3
                item.process_by = user
                item.save()
            return HttpResponseRedirect('operate_get')


def out_appointment(request):
    if not request.session.get('username'):
        return HttpResponseRedirect('login_in')

    if request.method == 'POST':
        context = {}
        context.update(csrf(request))
        a_status = request.POST.get('status')
        a_date_start = request.POST.get('date_start')
        a_date_end = request.POST.get('date_end')
        user = HomeAdmin.objects.get(username=request.session['username'])
        all_appointments = Appointment.objects.order_by('-id').filter(status=a_status, area=user.area)
        appointments = []
        print "OK1"
        if all_appointments.count() > 0:
            for item in all_appointments:
                it_date = str(item.create_time)[0:10]
                date_start = str(a_date_start)
                date_end = str(a_date_end)
                if date_start == date_end:
                    if it_date == date_start:
                        appointments.append(item)
                else:
                    if it_date >= date_start and it_date <= date_end:
                        appointments.append(item)

        print len(appointments)
        if a_status == '3':
            file_name = user.area.area_name + a_date_start + unicode('到', 'utf-8') + a_date_end + unicode('完成的预约', 'utf-8')
        else:
            file_name = user.area.area_name + a_date_start + unicode('到', 'utf-8') + a_date_end + unicode('取消的预约', 'utf-8')
        print file_name
        req = out_excel(appointments, file_name)
        if req:
            return HttpResponse(json.dumps('/out_files/'+file_name+'.xls'))


def out_excel(appointments, file_name):
    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet(file_name)
    style0 = xlwt.easyxf('font: name Times New Roman, color-index red, bold on')
    ws.write(0, 0, "预约号")
    ws.write(0, 1, "预约电话")
    ws.write(0, 2, "姓名")
    ws.write(0, 3, "地址")
    ws.write(0, 4, "时间")
    ws.write(0, 5, "预约状态")
    ws.write(0, 6, "地区")
    ws.write(0, 7, "操作员")
    ws.write(0, 8, "预约内容")
    i = 1
    for item in appointments:
        ws.write(i, 0, item.id, style0)
        ws.write(i, 1, item.consumer.phone, style0)
        ws.write(i, 2, item.name)
        ws.write(i, 3, item.address)
        it_date = str(item.create_time)[0:10]
        ws.write(i, 4, it_date)
        if item.status == '1':
            status_text = "未受理"
        elif item.status == '2':
            status_text = "已接受"
        elif item.status == '3':
            status_text = "已完成"
        else:
            status_text = "已取消"
        ws.write(i, 5, status_text, style0)
        ws.write(i, 6, item.area.area_name)
        ws.write(i, 7, item.process_by.nick)
        ws.write(i, 8, item.content)
        i += 1

    wb.save("out_files/"+file_name+".xls")
    return True

