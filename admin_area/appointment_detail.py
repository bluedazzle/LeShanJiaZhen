# -*- coding: utf-8 -*-
from views import *


def get_appointment(request):
    if request.method == 'GET':
        if request.session.get('username'):
            id = request.GET.get('id')
            appointment = Appointment.objects.get(id=id, status=1)
            appointment.status = 2
            appointment.save()
            return HttpResponseRedirect('operate_new')
        else:
            return HttpResponseRedirect('login_in')


def get_appointment_all(request):
    if request.method == 'GET':
        if request.session.get('username'):
            username = request.session['username']
            user = HomeAdmin.objects.get(username=username)
            appointments = Appointment.objects.filter(process_by=user, status=1)
            for item in appointments:
                item.status = 2
                item.save()
            return HttpResponseRedirect('operate_new')
        else:
            return HttpResponseRedirect('login_in')


def cancel_appointment_n(request):
    if request.method == 'GET':
        if request.session.get('username'):
            id = request.GET.get('id')
            appointment = Appointment.objects.get(id=id, status=1)
            appointment.status = 4
            appointment.save()
            return HttpResponseRedirect('operate_new')
        else:
            return HttpResponseRedirect('login_in')


def cancel_appointment_all_n(request):
    if request.method == 'GET':
        if request.session.get('username'):
            username = request.session['username']
            user = HomeAdmin.objects.get(username=username)
            appointments = Appointment.objects.filter(process_by=user, status=1)
            for item in appointments:
                item.status = 4
                item.save()
            return HttpResponseRedirect('operate_new')
        else:
            return HttpResponseRedirect('login_in')


def cancel_appointment_g(request):
    if request.method == 'GET':
        if request.session.get('username'):
            id = request.GET.get('id')
            appointment = Appointment.objects.get(id=id, status=2)
            appointment.status = 4
            appointment.save()
            return HttpResponseRedirect('operate_get')


def cancel_appointment_all_g(request):
    if request.method == 'GET':
        if request.session.get('username'):
            username = request.session['username']
            user = HomeAdmin.objects.get(username=username)
            appointments = Appointment.objects.filter(process_by=user, status=2)
            for item in appointments:
                item.status = 4
                item.save()
            return HttpResponseRedirect('operate_get')
        else:
            return HttpResponseRedirect('login_in')


def finish_appointment(request):
    if request.method == 'GET':
        if request.session.get('username'):
            id = request.GET.get('id')
            appointment = Appointment.objects.get(id=id, status=2)
            appointment.status = 3
            appointment.save()
            return HttpResponseRedirect('operate_get')


def finish_appointment_all(request):
    if request.method == 'GET':
        if request.session.get('username'):
            username = request.session['username']
            user = HomeAdmin.objects.get(username=username)
            appointments = Appointment.objects.get(process_by=user, status=2)
            for item in appointments:
                item.status = 3
                item.save()
            return HttpResponseRedirect('operate_get')
