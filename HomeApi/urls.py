from django.conf.urls import patterns, include, url
from HomeApi import views

urlpatterns = patterns('',
    url(r'^consumer/login$', views.login),
    url(r'^consumer/logout$', views.logout),
    url(r'^consumer/send_reg_verify$', views.send_reg_verify),
    url(r'^consumer/verify_reg_code$', views.verify_reg),
    url(r'^consumer/register$', views.register),
    url(r'^consumer/change_password$', views.change_password),
    url(r'^consumer/forget_password$', views.forget_password),
    url(r'^consumer/reset_password$', views.reset_password),
    url(r'^consumer/get_android_version$', views.get_android_version),
    url(r'^consumer/get_ios_version$', views.get_ios_version),
    url(r'^consumer/get_messages$', views.get_messages),
    url(r'^consumer/get_coupons$', views.get_coupon),
    url(r'^consumer/new_feedback$', views.add_feedback),
    url(r'^consumer/city_search$', views.city_search),
    url(r'^consumer/change_info$', views.change_info),
    url(r'^consumer/get_invite_coupon$', views.get_invite_coupon),
    url(r'^consumer/get_goods_item$', views.get_goods_p_item),
    url(r'^consumer/get_goods_detail$', views.get_goods),
    )