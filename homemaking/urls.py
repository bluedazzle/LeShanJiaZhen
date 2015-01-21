from django.conf.urls import patterns, include, url
from django.contrib import admin
from admin_area.views import *
import admin_all.urls
import admin_area.urls
import settings
from HomeApi.views import *

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'homemaking.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^master_admin/', include(admin_all.urls)),
    url(r'^$', index),
    url(r'^area_admin/', include(admin_area.urls)),
    # url(r'^add/', test_block),
    # url(r'^del/', del_block),
    # url(r'^ch/', change_block),
    url(r'^getnearest/', getnearest),
    url(r'^getcategory/', get_categories),
    url(r'^getitem/', get_detail_item),
    url(r'^area_tel/', pull_block_tel),
    url(r'^mkappoint/', make_appointment),
    url(r'^appointpic/', appointment_pic),
    url(r'^getverify/', send_phone_verify),
    url(r'^phoneverify/', verify_get_token),
    url(r'^getad/', pull_advertisement),
    # url(r'^master_admin/', include('admin_all.urls')),
    url(r'^css/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.CSS_DIR}),
    url(r'^img/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.IMG_DIR}),
    url(r'^js/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.JS_DIR}),
    url(r'^fonts/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.FONTS_DIR}),
    url(r'^out_files/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.OUT_FILES_DIR}),
)
