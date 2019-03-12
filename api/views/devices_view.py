from api.views.abstract_api_view import AbstractAPIView
from api.forms.devices_form import DevicesForm
from api.helpers.devices import DevicesHelper

class Devices(AbstractAPIView):
    """
        Highest total pageviews API form for handle request
    """
    success = 'Get total devices by timerange succesfully.'
    failure = 'Get total devices by timerange failed.'
    def post(self, request):
        form = DevicesForm(request.data)
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

        data = DevicesHelper().get_devices(number, start_time, end_time, page)

        return self.json_format(code=200, data=data, message=self.success, errors=[])