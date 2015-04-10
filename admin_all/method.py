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
        file_name = ''
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
                    if it_date >= date_start:
                        appointments.append(item)
                else:
                    if it_date >= date_start and it_date <= date_end:
                        appointments.append(item)

        print len(appointments)
        if a_date_start == '2000-01-01' and a_date_end == '2999-11-11':
            file_name = area.area_name + unicode("全部时间的", 'utf-8')
        else:
            file_name = area.area_name + a_date_start + unicode("到", "utf-8") + a_date_end

        if a_status == 1:
            file_name += unicode("未接受的订单", "utf-8")
        elif a_status == 2:
            file_name += unicode("已接受的订单", "utf-8")
        elif a_status == 4:
            file_name += unicode("完成的订单", "utf-8")
        elif a_status == 5:
            file_name += unicode("取消的订单", "utf-8")
        elif a_status == 6:
            file_name += unicode("已评价订单", "utf-8")
        else:
            file_name += u'所有状态的预约'

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
    ws.write(0, 11, "评价")
    ws.write(0, 12, "评价选项")
    ws.write(0, 13, "评价内容")
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
        elif item.status == 4:
            status_text = u"已完成"
        elif item.status == 5:
            status_text = u"已取消"
        elif item.status == 6:
            status_text = u"已评价"
        else:
            status_text = u"未知"

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
        ws.write(i, 13, item.comment)
        i += 1

    wb.save("out_files/"+file_name+".xls")
    return True
