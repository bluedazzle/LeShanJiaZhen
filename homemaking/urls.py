from django.conf.urls import patterns, include, url
from django.contrib import admin
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
    url(r'^area_admin/', include(admin_area.urls)),
    url(r'^add/', test_block),
    #url(r'^del/', del_block),
    # url(r'^ch/', change_block),
    url(r'^getnearest/', getnearest),
    url(r'^fullcorrespond/', get_the_full_corresponding),
    url(r'^area_tel/', pull_block_tel),
    url(r'^mkappoint/', make_appointment),
    url(r'^getad/', pull_advertisement),
    # url(r'^master_admin/', include('admin_all.urls')),
    url(r'^css/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.CSS_DIR}),
    url(r'^img/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.IMG_DIR}),
    url(r'^js/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.JS_DIR}),
    url(r'^fonts/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.FONTS_DIR}),
    url(r'^out_files/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.OUT_FILES_DIR}),
)
