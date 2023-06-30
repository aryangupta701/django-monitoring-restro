from django.db import models

class StoreBusinessHours(models.Model):
    store_id = models.CharField(max_length=255)
    day = models.IntegerField()
    start_time_local = models.TimeField()
    end_time_local = models.TimeField()

    def __str__(self):
        return f"StoreBusinessHours: {self.store_id} - {self.day} - {self.start_time_local} - {self.end_time_local}"


class StoreTimezone(models.Model):
    store_id = models.CharField(max_length=255)
    timezone_str = models.CharField(max_length=255) 

    def __str__(self):
        return f"StoreTimezone: {self.store_id} - {self.timezone_str}"

class StoreStatus(models.Model):
    store_id = models.CharField(max_length=255)
    status = models.CharField(max_length=255)
    timestamp_utc = models.DateTimeField()

    def __str__(self):
        return f"StoreStatus: {self.store_id} - {self.status} - {self.timestamp_utc}"

class Report(models.Model):
    report_id = models.CharField(max_length=255, unique=True)
    csv_file = models.FileField(upload_to='reports/')
    isProcessing = models.BooleanField(default=False)
    isGenerated = models.BooleanField(default=False)

    def __str__(self):
        return f"Report ID: {self.report_id}"