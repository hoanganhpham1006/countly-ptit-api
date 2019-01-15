from django.urls import path
from api.views.total_view import Total

app_name = 'api'

urlpatterns = [
    path('total', Total.as_view(), name='total-page-views'),
]
