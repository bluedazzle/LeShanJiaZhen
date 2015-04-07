# -*- coding: utf-8 -*-
from views import *
import xlwt
import sys
reload(sys)
sys.setdefaultencoding('utf-8')


def send_get_message(appointments):
    apikey = 'e1ebef39f28c86fdb57808eb45ab713a'
    for appointment in appointments:
        content = "#order_num#=" + appointment.order_id
        res = tpl_send_sms(apikey, '669219', content, appointment.order_phone)
        jsres = simplejson.loads(res)
        msg = jsres['code']
        print jsres
        print msg
    return True


def send_cancel_message(appointments):
    apikey = 'e1ebef39f28c86fdb57808eb45ab713a'
    for appointment in appointments:
        content = "#order_num#=" + appointment.order_id
        res = tpl_send_sms(apikey, '669219', content, appointment.order_phone)
        jsres = simplejson.loads(res)
        msg = jsres['code']
        print jsres
        print msg
    return True


def get_appointment(request):
    if request.method == 'GET':
        if request.session.get('username'):
            id = request.GET.get('id')
            try:
                user = HomeAdmin.objects.get(username=request.session['username'])
                appointment = Appointment.objects.get(id=id, status=1)
                appointment.status = 2
                appointment.process_by = user
                appointment.save()
                appointments = [appointment]
                if send_get_message(appointments):
                    return HttpResponseRedirect('operate_new')
            except:
                return HttpResponseRedirect('operate_new')
        else:
            return HttpResponseRedirect('login_in')
    else:
        raise Http404


def get_appointment_all(request):
    if request.method == 'GET':
        if request.session.get('username'):
            username = request.session['username']
            user = HomeAdmin.objects.get(username=username)
            appointments = Appointment.objects.filter(area=user.area, status=1)
            if appointments.count() == 0:
                return HttpResponseRedirect('operate_new')
            for item in appointments:
                item.status = 2
                item.process_by = user
                item.save()
            # try:
            #     send_get_message(appointments)
            # except:
            #     pass
            return HttpResponseRedirect('operate_new')
        else:
            return HttpResponseRedirect('login_in')


def cancel_appointment_n(request):
    if request.method == 'GET':
        if request.session.get('username'):
            id = request.GET.get('id')
            user = HomeAdmin.objects.get(username=request.session['username'])
            try:
                appointment = Appointment.objects.get(id=id, status=1)
                appointment.status = 4
                appointment.process_by = user
                appointment.save()
                appointments = [appointment]
                send_cancel_message(appointments)
            except:
                return HttpResponseRedirect('operate_new')
            return HttpResponseRedirect('operate_new')
        else:
            return HttpResponseRedirect('login_in')


def cancel_appointment_all_n(request):
    if request.method == 'GET':
        if request.session.get('username'):
            username = request.session['username']
            user = HomeAdmin.objects.get(username=username)
            appointments = Appointment.objects.filter(area=user.area, status=1)
            if appointments.count() == 0:
                return HttpResponseRedirect('operate_get')

            for item in appointments:
                item.status = 4
                item.area = user.area
                item.save()
            # try:
            #     send_cancel_message(appointments)
            # except:
            #     pass
            return HttpResponseRedirect('operate_get')
        else:
            return HttpResponseRedirect('login_in')


def cancel_appointment_g(request):
    if request.method == 'GET':
        if request.session.get('username'):
            id = request.GET.get('id')
            user = HomeAdmin.objects.get(username=request.session['username'])
            try:
                appointment = Appointment.objects.get(id=id, status=2)
                appointment.status = 4
                appointment.process_by = user
                appointment.save()
                send_cancel_message([appointment])
            except:
                pass
            return HttpResponseRedirect('operate_get')


def cancel_appointment_all_g(request):
    if request.method == 'GET':
        if request.session.get('username'):
            username = request.session['username']
            user = HomeAdmin.objects.get(username=username)
            appointments = Appointment.objects.filter(area=user.area, status=2)
            if appointments.count() == 0:
                return HttpResponseRedirect('operate_get')

            for item in appointments:
                item.status = 4
                item.process_by = user
                item.save()

            try:
                send_cancel_message(appointments)
            except:
                pass
            return HttpResponseRedirect('operate_get')
        else:
            return HttpResponseRedirect('login_in')


def finish_appointment(request):
    if request.method == 'GET':
        if request.session.get('username'):
            user = HomeAdmin.objects.get(username=request.session['username'])
            id = request.GET.get('id')
            try:
                appointment = Appointment.objects.get(id=id, status=2)
                appointment.status = 3
                appointment.process_by = user
                appointment.save()
            except:
                pass
            return HttpResponseRedirect('operate_get')
        else:
            return HttpResponseRedirect('login_in')


def appointment_add_info(request):
    if request.method == 'GET':
        if request.session.get('username'):
            user = HomeAdmin.objects.get(username=request.session['username'])
            id = request.GET.get('aid')
            s_person = request.GET.get('service_person')
            s_time = request.GET.get('service_time')
            page = request.GET.get('page')
            appointment = Appointment.objects.get(id=id, status=2)
            appointment.service_person = s_person
            appointment.service_time = s_time
            appointment.save()
            return HttpResponseRedirect('operate_get?page='+page)
        else:
            return HttpResponseRedirect('login_in')


def finish_appointment_all(request):
    if request.method == 'GET':
        if request.session.get('username'):
            username = request.session['username']
            user = HomeAdmin.objects.get(username=username)
            appointments = Appointment.objects.filter(area=user.area, status=2)
            if appointments.count() == 0:
                return HttpResponseRedirect('operate_get')

            for item in appointments:
                item.status = 3
                item.process_by = user
                item.save()
            return HttpResponseRedirect('operate_get')
        else:
            return HttpResponseRedirect('login_in')


def out_appointment(request):
    if not request.session.get('username'):
        return HttpResponseRedirect('login_in')

    if request.method == 'POST':
        context = {}
        context.update(csrf(request))
        a_status = request.POST.get('status')
        a_date_start = request.POST.get('date_start')
        a_date_end = request.POST.get('date_end')
        end_time = time.strptime(a_date_end, "%Y-%m-%d")
        start_time = time.strptime(a_date_start, "%Y-%m-%d")
        end_time = datetime.datetime(*end_time[:6])
        start_time = datetime.datetime(*start_time[:6])
        if_appraise = request.POST.get('if_appraise')
        user = HomeAdmin.objects.get(username=request.session['username'])
        if if_appraise:
            if end_time == start_time:
                all_appointments = Appointment.objects.order_by('-id').filter(status=a_status,
                                                                              area=user.area,
                                                                              if_appraise=True,
                                                                              create_time__gte=start_time)
            else:
                all_appointments = Appointment.objects.order_by('-id').filter(status=a_status,
                                                                              area=user.area,
                                                                              if_appraise=True,
                                                                              create_time__lte=end_time,
                                                                              create_time__gte=start_time)
        else:
            if end_time == start_time:
                all_appointments = Appointment.objects.order_by('-id').filter(status=a_status,
                                                                              area=user.area,
                                                                              create_time__gte=start_time)
            else:
                all_appointments = Appointment.objects.order_by('-id').filter(status=a_status,
                                                                              area=user.area,
                                                                              create_time__lte=end_time,
                                                                              create_time__gte=start_time)
        print "OK1"

        print all_appointments.count()
        print start_time
        print end_time
        if a_status == '3':
            if a_date_start == '2000-01-01' and a_date_end == '2999-11-11':
                if if_appraise:
                    file_name = user.area.area_name + unicode("所有评价的订单", 'utf-8')
                else:
                    file_name = user.area.area_name + unicode("所有完成的订单", 'utf-8')
            else:
                if if_appraise:
                    file_name = user.area.area_name + a_date_start + unicode("到", 'utf-8') + a_date_end + unicode("评价的订单", 'utf-8')
                else:
                    file_name = user.area.area_name + a_date_start + unicode("到", 'utf-8') + a_date_end + unicode("完成的订单", 'utf-8')
        else:
            if a_date_start == '2000-01-01' and a_date_end == '2999-11-11':
                file_name = user.area.area_name + unicode("所有取消的订单", 'utf-8')
            else:
                file_name = user.area.area_name + a_date_start + unicode("到", 'utf-8') + a_date_end + unicode("取消的订单", 'utf-8')
        print file_name
        req = out_excel(all_appointments, file_name)
        if req:
            return HttpResponse(json.dumps('/out_files/'+file_name+'.xls'))


def out_excel(appointments, file_name):
    wb = xlwt.Workbook(encoding='utf-8')
    now_time = time.time()
    ws = wb.add_sheet(str(now_time))
    style0 = xlwt.easyxf('font: name Times New Roman, color-index red, bold on')
    ws.write(0, 0, "订单号")
    ws.write(0, 1, "订单类型")
    ws.write(0, 2, "联系电话")
    ws.write(0, 3, "姓名")
    ws.write(0, 4, "地址")
    ws.write(0, 5, "下单时间")
    ws.write(0, 6, "订单状态")
    ws.write(0, 7, "地区")
    ws.write(0, 8, "操作员")
    ws.write(0, 9, "订单内容")
    ws.write(0, 10, "备注")
    ws.write(0, 11, "评价")
    ws.write(0, 12, "评价内容")
    i = 1
    for item in appointments:
        ws.write(i, 0, item.order_id, style0)
        ws.write(i, 2, item.order_phone, style0)
        if item.orderitem.all().count() > 0:
            ws.write(i, 1, u"维修安装")
        else:
            ws.write(i, 1, u"商品购买")
        ws.write(i, 3, item.name)
        ws.write(i, 4, item.address)
        it_date = str(item.create_time)[0:10]
        ws.write(i, 5, it_date)
        if item.status == 1:
            status_text = u"未接受"
        elif item.status == 2:
            status_text = u"已接受"
        elif item.status == 3:
            status_text = u"已完成"
        else:
            status_text = u"已取消"
        ws.write(i, 6, status_text, style0)
        ws.write(i, 7, item.area.area_name)
        if item.process_by:
            ws.write(i, 8, item.process_by.nick)
        else:
            ws.write(i, 8, '')
        content = ''
        print 'ok'
        if item.orderitem.all().count() > 0:
            for orderitem in item.orderitem.all():
                content = content + orderitem.item_name + '\t\t'
        elif item.ordergoods.all().count > 0:
            for goods in item.ordergoods.all():
                content = content + goods.title + '\t\t'

        ws.write(i, 9, content)
        ws.write(i, 10, item.remark)
        content = ''
        if item.if_appraise:
            ws.write(i, 11, item.rate)
            if item.rb1:
                content += u"上门及时；"
            if item.rb2:
                content += u"认真仔细；"
            if item.rb3:
                content += u"技术专业；"
            if item.rb4:
                content += u"收费公道；"
            if item.rb5:
                content += u"维修快速；"
            if item.rb6:
                content += u"态度良好；"
        else:
            ws.write(i, 11, '')
        ws.write(i, 12, content)
        i += 1

    wb.save("out_files/"+file_name+".xls")
    return True

