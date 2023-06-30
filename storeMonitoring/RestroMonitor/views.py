from django.http import JsonResponse, HttpResponse
from django.views import View
import uuid
from .tasks import generate_report
from .models import Report, StoreStatus
import asyncio
from asgiref.sync import sync_to_async
import base64

class TriggerReportView(View):
    def post(self, request):
        report_id = self.generate_report_id()

        report = Report(report_id=report_id, isProcessing=True)
        report.save()
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.create_task(sync_to_async(generate_report)(report_id))
        loop.run_until_complete(asyncio.gather())

        return JsonResponse({'report_id': report_id})
    
    def generate_report_id(self):
        return str(uuid.uuid4())

class GetReportView(View):
    def get(self, request, report_id):
        try:
            report = Report.objects.get(report_id=report_id)
            if report.isProcessing :
                return JsonResponse({'status': 'Running'})
            if report.isGenerated == False : 
                return JsonResponse({'status': 'Report Not Generated'})
            else:
                csv_data = report.csv_file.read()
                return JsonResponse({'status': str(csv_data)})

        except Exception as e:
            return JsonResponse({'Error': e})