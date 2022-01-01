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
            print(e.json())
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
    return HttpResponse('This method use POST method', status=400)


@csrf_exempt
def correlation(request: HttpRequest) -> JsonResponse | None:
    return None
