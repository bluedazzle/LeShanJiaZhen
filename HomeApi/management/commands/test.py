from django.core.management.base import BaseCommand
from HomeApi.views import *
from HomeApi.OnlinePay import *


class Command(BaseCommand):
    def handle(self, *args, **options):
        rse = refund_order('ch_8qHyv9Tm5yT0T04abLOSabDO', 'test', 1)
        print rse