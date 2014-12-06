# -*- coding: utf-8 -*-
from views import *


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
