from django.shortcuts import render_to_response
from django.views.decorators.csrf import csrf_exempt
from models import *

# Create your views here.


def login_in(request):
    if request.method == 'GET':
        return render_to_response('master_login.html')


def find_appointment(request):
    if request.method == 'GET':
        items = range(0, 10)
        return render_to_response('admin_all/find_appointment.html', {'items': items})


def manage_admin(request):
    if request.method == 'GET':
        items = range(0, 10)
        return render_to_response('admin_all/manage_admin.html', {'items': items})


def manage_apply(request):
    if request.method == 'GET':
        items = range(0, 10)
        return render_to_response('admin_all/manage_apply.html', {'items': items})


def about(request):
    if request.method == 'GET':
        return render_to_response('admin_all/about.html')