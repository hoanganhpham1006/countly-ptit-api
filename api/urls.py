from django.urls import path
from api.views.total_view import Total
from api.views.timerange_total_view import TimerangeTotal
from api.views.devices_view import Devices

app_name = 'api'

urlpatterns = [
    path('total', Total.as_view(), name='total-page-views'),
    path('timerange_total', TimerangeTotal.as_view(), name='timerange-total-page-views'),
    path('devices', Devices.as_view(), name='devices-page-views'),
]
