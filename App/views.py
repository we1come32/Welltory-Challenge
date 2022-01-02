import json

from django.http import JsonResponse, HttpResponse, HttpRequest
from django.views.decorators.csrf import csrf_exempt
from pydantic import ValidationError
from .models import *
from .pydantic_models import Data


@csrf_exempt
def calculate(request: HttpRequest) -> HttpResponse:
    if request.method == 'POST':
        try:
            data = Data(**json.loads(request.body.decode("utf-8")))
        except ValidationError as e:
            return HttpResponse("Unknown data format", status=400)
        try:
            user = DjangoUser.objects.get(id=data.user_id)
        except DjangoUser.DoesNotExist:
            return HttpResponse("Unknown user_id parameter", status=400)
        user = User.objects.get_or_create(user=user)[0]
        if user.add_data(name=data.data.x_data_type, values=data.data.x) and \
                user.add_data(name=data.data.y_data_type, values=data.data.y):
            return HttpResponse('ok')
        return HttpResponse('Unknown error', status=500)
    return HttpResponse('This method must be POST', status=400)


@csrf_exempt
def correlation(request: HttpRequest) -> HttpResponse | JsonResponse | None:
    if request.method == 'GET':
        if user_id := request.GET.get('user_id', False):
            try:
                user = DjangoUser.objects.get(id=int(user_id))
            except (DjangoUser.DoesNotExist, ValueError):
                return HttpResponse("Unknown user_id parameter", status=400)
            user = User.objects.get_or_create(user=user)[0]
            try:
                x = request.GET.get('x_data_type')
                y = request.GET.get('y_data_type')
            except KeyError:
                return HttpResponse("Unknown keys", status=400)
            r = user.get_correlation([x, y])
            return JsonResponse({
                'user_id': int(user_id),
                'x_data_type': x,
                'y_data_type': y,
                'correlation': {
                    'value': r[0][0],
                    'p_value': r[0][1]
                }
            })
        else:
            return HttpResponse("Unknown user_id parameter", status=400)
    return HttpResponse('This method must be GET', status=400)
