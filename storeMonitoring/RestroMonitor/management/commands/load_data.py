from django.core.management.base import BaseCommand
from RestroMonitor.models import StoreBusinessHours, StoreTimezone, StoreStatus
import csv
import os 
import pytz
from datetime import datetime

class Command(BaseCommand):
    def handle(self, *args, **options):
        current_dir = os.path.dirname(os.path.abspath(__file__))
        Menuhours= os.path.join(current_dir, 'data/Menuhours.csv')
        storestatus= os.path.join(current_dir, 'data/storestatus.csv')
        timezones= os.path.join(current_dir, 'data/timezones.csv')

        with open(Menuhours, 'r') as file:
            reader = csv.reader(file)
            flag = True
            for row in reader:
                try:
                    if(flag):
                        flag = False
                        continue
                    model = StoreBusinessHours(
                        store_id=row[0],
                        day=int(row[1]),
                        start_time_local=row[2],
                        end_time_local=row[3]
                    )
                    model.save()
                except Exception as e:
                    print(e)


        with open(storestatus, 'r') as file:
            reader = csv.reader(file)
            flag = True
            for row in reader:
                try:
                    if(flag):
                        flag = False
                        continue
                    try:
                        timestamp_utc=datetime.strptime(row[2], '%Y-%m-%d %H:%M:%S.%f %Z').replace(tzinfo=pytz.UTC)
                    except Exception as e:   
                        timestamp_utc=datetime.strptime(row[2], '%Y-%m-%d %H:%M:%S %Z').replace(tzinfo=pytz.UTC)
                    model = StoreStatus(
                        store_id=row[0],
                        status=row[1],
                        timestamp_utc=timestamp_utc
                    )
                    model.save()
                except Exception as e:
                    print(e)

        with open(timezones, 'r') as file:
            reader = csv.reader(file)
            flag = True
            for row in reader:
                try:
                    if(flag):
                        flag = False
                        continue
                    model = StoreTimezone(
                        store_id=row[0],
                        timezone_str=row[1]
                    )
                    model.save()
                except Exception as e:
                    print(e)
