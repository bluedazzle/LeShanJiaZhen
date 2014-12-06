from django.conf.urls import patterns, include, url
from views import *


urlpatterns = patterns('',
                       url('^login_in$', login_in),
                       url('^find_appointment$', find_appointment),
                       url('^manage_admin$', manage_admin),
                       url('^manage_apply$', manage_apply),
                       url('^about$', about),
                       )
