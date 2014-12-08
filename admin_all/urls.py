from django.conf.urls import patterns, include, url
from views import *
from method import *


urlpatterns = patterns('',
                       url('^login_in$', login_in),
                       url('^find_appointment$', find_appointment),
                       url('^manage_admin$', manage_admin),
                       url('^manage_apply$', manage_apply),
                       url('^manage_notice$', manage_notice),
                       url('^delete_admin$', delete_admin),
                       url('^pass_application$', pass_application),
                       url('^reject_application$', delete_application),
                       url('^delete_notices$', delete_notice),
                       url('^put_notice$', put_notice),
                       url('^out_appointment$', out_appointment),
                       )
