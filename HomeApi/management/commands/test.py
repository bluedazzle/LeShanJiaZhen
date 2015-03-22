from django.core.management.base import BaseCommand
from HomeApi.views import *


class Command(BaseCommand):
    def handle(self, *args, **options):
        create_order_id()