from django.contrib import admin
from HomeApi.models import *
# Register your models here.
class PhoneVerifyAdmin(admin.ModelAdmin):
    list_display = ('phone', 'verify', 'update_time')
    list_filter = ('update_time',)
    ordering = ('-update_time',)

admin.site.register(HomeAdmin)
admin.site.register(HomeItem_P)
admin.site.register(HomeItem_O)
admin.site.register(HomeItem)
admin.site.register(Advertisement)
admin.site.register(Appointment)
admin.site.register(Block)
admin.site.register(Notice)
# admin.site.register(PhoneVerify, PhoneVerifyAdmin)
admin.site.register(Consumer)
admin.site.register(Application)
admin.site.register(Message)
admin.site.register(Associator)
admin.site.register(Coupon)
admin.site.register(CouponControl)
admin.site.register(Goods_P)
admin.site.register(Goods_O)
admin.site.register(GoodsItem)
admin.site.register(Feedback)
admin.site.register(AppControl)
admin.site.register(Verify)

