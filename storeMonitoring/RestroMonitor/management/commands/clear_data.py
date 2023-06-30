from RestroMonitor.models import StoreBusinessHours, StoreTimezone, StoreStatus
from django.core.management.base import BaseCommand

class Command(BaseCommand):
    def handle(self, *args, **options):
        StoreBusinessHours.objects.all().delete()
        StoreTimezone.objects.all().delete()
        StoreStatus.objects.all().delete()
