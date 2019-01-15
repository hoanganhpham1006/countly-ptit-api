from api.forms.abstract_form import AbstractForm
from django import forms

class TotalForm(AbstractForm):
    number = forms.IntegerField(required=False, initial=10)
    total_type = forms.CharField(required=False, initial='all')
    page = forms.IntegerField(required=False, initial=1)

