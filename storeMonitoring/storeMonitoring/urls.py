from django.urls import path
from RestroMonitor.views import TriggerReportView, GetReportView

from django.contrib import admin


urlpatterns = [
    path('admin/', admin.site.urls),
    path('trigger_report/', TriggerReportView.as_view(), name='trigger_report'),
    path('get_report/<str:report_id>/', GetReportView.as_view(), name='get_report'),
]
