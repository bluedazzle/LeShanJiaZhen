# -*- coding: utf-8 -*-
import xlwt
from views import *
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import time


def out_appointment(request):
    if not request.session.get('a_username'):
        return HttpResponseRedirect('login_in')

    if request.method == 'POST':
        context = {}
        context.update(csrf(request))
        print "OK"
        a_status = request.POST.get('status')
        a_date_start = request.POST.get('date_start')
        a_date_end = request.POST.get('date_end')
        area_name = request.POST.get('area')
        area = Block.objects.get(area_name=area_name)
        if a_status == '0':
            all_appointments = Appointment.objects.order_by('-id').filter(area=area)
        else:
            all_appointments = Appointment.objects.order_by('-id').filter(status=a_status, area=area)
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
        if a_status == 1:
            file_name = area.area_name + a_date_start + unicode("到", "utf-8") + a_date_end + unicode("未接受的订单", "utf-8")
        elif a_status == 2:
            file_name = area.area_name + a_date_start + unicode("到", "utf-8") + a_date_end + unicode("已接受的订单", "utf-8")
        elif a_status == 3:
            file_name = area.area_name + a_date_start + unicode("到", "utf-8") + a_date_end + unicode("完成的订单", "utf-8")
        elif a_status == 4:
            file_name = area.area_name + a_date_start + unicode("到", "utf-8") + a_date_end + unicode("取消的订单", "utf-8")
        else:
            file_name = area.area_name + a_date_start + u'到' + a_date_end + u'所有预约'

        print file_name
        req = out_excel(appointments, file_name)
        if req:
            return HttpResponse(json.dumps('/out_files/'+file_name+'.xls'))


def out_excel(appointments, file_name):
    wb = xlwt.Workbook(encoding='utf-8')
    now_time = time.clock()
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
    i = 1
    for item in appointments:
        ws.write(i, 0, item.order_id, style0)
        if item.consumer:
            ws.write(i, 2, item.consumer.phone, style0)
        else:
            ws.write(i, 2, item.associator.username, style0)
        if item.orderhomeitems.all().count() > 0:
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
        ws.write(i, 8, item.process_by.nick)
        content = ''
        print 'ok'
        if item.orderhomeitems.all().count() > 0:
            for orderhomeitem in item.orderhomeitems.all():
                content = content + orderhomeitem.title + '\t\t'
        elif item.ordergoods.all().count > 0:
            for goods in item.ordergoods.all():
                content = content + goods.title + '\t\t'

        ws.write(i, 9, content)
        ws.write(i, 10, item.remark)
        i += 1

    wb.save("out_files/"+file_name+".xls")
    return True
