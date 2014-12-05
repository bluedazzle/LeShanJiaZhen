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
admin.site.register(Advertisment)
admin.site.register(Appointment)
admin.site.register(Block)
admin.site.register(Notice)
admin.site.register(PhoneVerify, PhoneVerifyAdmin)
admin.site.register(Consumer)