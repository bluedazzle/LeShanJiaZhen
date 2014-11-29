from django.conf.urls import patterns, url
from views import *


urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'homemaking.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url('^login_in$', login_in),
    url('^register$', register),
    url('^forget_password$', forget_password),
    url('^operate_new$', operate_new),
)