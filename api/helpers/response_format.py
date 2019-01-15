from django.http import JsonResponse

def json_format(code = 200, message = 'Bingo! Default message.', data = None, errors = None):
    return JsonResponse({
        'code': code,
        'data': data,
        'message': message,
        'errors': errors
    }, status=code)

def total_array_format(views=None, viewcounts=None, total_type=None):
    return [{'views':views, 'viewcounts':viewcounts, 'total_type':total_type}]