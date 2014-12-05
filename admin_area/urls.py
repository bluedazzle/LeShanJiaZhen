from django.conf.urls import patterns, include, url
from views import *
from appointment_detail import *


urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'homemaking.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url('^login_in$', login_in),
    url('^register$', register),
    url('^forget_password$', forget_password),
    url('^operate_new$', operate_new),
    url('^operate_get$', operate_get),
    url('^operate_finish$', operate_finish),
    url('^operate_cancel$', operate_cancel),
    url('^user_mes$', user_mes),
    url('^about$', about),
    url('^register_verify$', phone_verify),
    url('^f_register_verify$', f_phone_verify),
    url('^get_new_appointment$', get_new_appointment),
    url('^get_new_appointment_count$', get_new_appointment_count),
    url('^appointment_get$', get_appointment),
    url('^appointment_cancel_n$', cancel_appointment_n),
    url('^appointment_cancel_g$', cancel_appointment_g),
    url('^appointment_finish$', finish_appointment),
    url('^appointment_get_all$', get_appointment_all),
    url('^appointment_cancel_all_n$', cancel_appointment_all_n),
    url('^appointment_cancel_all_g$', cancel_appointment_all_g),
    url('^appointment_finish_all$', finish_appointment_all),
)