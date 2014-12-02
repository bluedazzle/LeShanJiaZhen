from django.conf.urls import patterns, include, url
from django.contrib import admin
from admin_all import urls
from HomeApi.views import *
import settings

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'homemaking.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    # url(r'^master_admin/', include('admin_all.urls')),
    url(r'^area_admin/', include('admin_area.urls')),
    url(r'^css/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.CSS_DIR}),
    url(r'^img/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.IMG_DIR}),
    url(r'^js/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.JS_DIR}),
    url(r'^fonts/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.FONTS_DIR}),
)
