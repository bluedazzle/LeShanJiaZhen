from django.conf.urls import patterns, include, url
from views import *


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
)