from django.urls import path
from api.views.total_view import Total
from api.views.timerange_total_view import TimerangeTotal

app_name = 'api'

urlpatterns = [
    path('total', Total.as_view(), name='total-page-views'),
    path('timerange_total', TimerangeTotal.as_view(), name='timerange-total-page-views'),
]
