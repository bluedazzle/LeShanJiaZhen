from django.shortcuts import render_to_response
from django.views.decorators.csrf import csrf_exempt
from models import *


def login_in(request):
    if request.method == 'GET':
        return render_to_response('login_in.html')


def register(request):
    if request.method == 'GET':
        return render_to_response('register.html')


def forget_password(request):
    if request.method == 'GET':
        return render_to_response('forget_password.html')


def operate_new(request):
    if request.method == 'GET':
        items = [1, 2, 3, 4, 5, 6]
        return render_to_response('admin_area/operate_new.html', {'items': items})


def operate_get(request):
    if request.method == 'GET':
        items = [1, 2, 3, 4, 5, 6]
        return render_to_response('admin_area/operate_get.html', {'items': items})


def operate_finish(request):
    if request.method == 'GET':
        items = [1, 2, 3, 4, 5, 6]
        return render_to_response('admin_area/operate_finish.html', {'items': items})


def operate_cancel(request):
    if request.method == 'GET':
        items = [1, 2, 3, 4, 5, 6]
        return render_to_response('admin_area/operate_cancel.html', {'items': items})


def user_mes(request):
    if request.method == 'GET':
        return render_to_response('admin_area/user_mes.html')


def about(request):
    if request.method == 'GET':
        return render_to_response('admin_area/about.html')