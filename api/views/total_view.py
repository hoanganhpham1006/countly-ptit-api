from api.views.abstract_api_view import AbstractAPIView
from api.forms.total_form import TotalForm
from api.helpers.total import TotalHelper

class Total(AbstractAPIView):
    """
        Highest total pageviews API form for handle request
    """
    success = 'Get total pageviews succesfully.'
    failure = 'Get total pageviews failed.'
    def post(self, request):
        form = TotalForm(request.data)
        if not form.is_valid():
            return self.json_format(code=442, data=[], message=self.failure, errors = form.errors)

        number = form.cleaned_data.get('number')
        total_type = form.cleaned_data.get('total_type')
        page = form.cleaned_data.get('page')

        if number is None:
            number = 10
        if total_type == '':
            total_type = 'all'
        if page is None:
            page = 1
            
        data = TotalHelper().get_total(number, total_type, page)

        return self.json_format(code=200, data=data, message=self.success, errors=[])