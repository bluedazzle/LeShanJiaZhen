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