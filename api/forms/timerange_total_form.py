from api.forms.abstract_form import AbstractForm
from django import forms

class TimerangeTotalForm(AbstractForm):
    number = forms.IntegerField(required=False, initial=10)
    page = forms.IntegerField(required=False, initial=1)
    start_time = forms.CharField(required=True)
    end_time = forms.CharField(required=True)

