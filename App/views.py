from typing import List
from datetime import date

from django.http import JsonResponse, HttpResponse, HttpRequest
from pydantic import BaseModel, ValidationError


class Value(BaseModel):
    date: date
    value: float


class MassValue(BaseModel):
    x_data_type: str
    y_data_type: str
    x: List[Value]
    y: List[Value]


class Data(BaseModel):
    user_id: int
    data: MassValue


def calculate(request: HttpRequest) -> HttpResponse:
    if request.method == 'POST':
        try:
            a = Data(**request.POST)
        except ValidationError:
            return HttpResponse("Unknown data format", status=400)
        return HttpResponse('ok')
    return HttpResponse('This method use POST method', status=400)


def correlation(request: HttpRequest) -> JsonResponse | None:
    return None
