from django.conf.urls import patterns, include, url
from HomeApi import views
from HomeApi import OnlinePay

urlpatterns = patterns('',
    url(r'^consumer/login$', views.login),
    url(r'^consumer/logout$', views.logout),
    url(r'^consumer/send_verify$', views.send_consumer_verify),
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
    url(r'^consumer/get_city_list$', views.get_all_city),
    url(r'^consumer/change_info$', views.change_info),
    url(r'^consumer/get_invite_coupon$', views.get_invite_coupon),
    url(r'^consumer/get_goods_item$', views.get_goods_p_item),
    url(r'^consumer/get_goods_sec_item$', views.get_goods_o_item),
    url(r'^consumer/get_goods_detail$', views.get_goods_detail),
    url(r'^consumer/create_pay_order$', views.create_pay_order),
    url(r'^consumer/create_appointment$', views.create_appointment),
    url(r'^consumer/upload_picture$', views.appointment_pic),
    url(r'^consumer/verify_consumer$', views.verify_consumer),
    url(r'^consumer/get_charge_status$', views.status_search),
    url(r'^consumer/get_homeitem$', views.get_home_item_p),
    url(r'^consumer/get_unread_message_count$', views.get_unread_message_count),
    url(r'^consumer/read_message$', views.read_message),
    url(r'^consumer/get_homeitem_detail$', views.get_home_item),
    url(r'^consumer/get_recommand$', views.get_recommmand_list),
    url(r'^consumer/get_advertisment$', views.get_advertisment),
    url(r'^consumer/appraise$', views.appraise),
    url(r'^consumer/get_all_orders$', views.get_orders),
    url(r'^consumer/check_game$', views.check_game),
    url(r'^consumer/play_game$', views.play_game),
    url(r'^consumer/cancel_order$', views.cancel_order),
    url(r'^pingpp/charge_result$', OnlinePay.charge_result),
    )