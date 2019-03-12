from api.views.abstract_api_view import AbstractAPIView
from api.forms.timerange_total_form import TimerangeTotalForm
from api.helpers.timerange_total import TimerangeTotalHelper

class TimerangeTotal(AbstractAPIView):
    """
        Highest total pageviews API form for handle request
    """
    success = 'Get total pageviews by timerange succesfully.'
    failure = 'Get total pageviews by timerange failed.'
    def post(self, request):
        form = TimerangeTotalForm(request.data)
        if not form.is_valid():
            return self.json_format(code=442, data=[], message=self.failure, errors = form.errors)

        number = form.cleaned_data.get('number') + 1
        page = form.cleaned_data.get('page')
        start_time = form.cleaned_data.get('start_time')
        end_time = form.cleaned_data.get('end_time')

        if number is None:
            number = 11
        if page is None:
            page = 1

        data = TimerangeTotalHelper().get_timerange_total(number, start_time, end_time, page)

        return self.json_format(code=200, data=data, message=self.success, errors=[])