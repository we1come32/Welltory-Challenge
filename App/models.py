from typing import Dict, List
import numpy as np

from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User as DjangoUser

from .pydantic_models import Value as PydanticValue


class User(models.Model):
    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
    user = models.ForeignKey(DjangoUser, on_delete=models.CASCADE, verbose_name='Пользователь', related_name='tbrgfj')

    def get_correlation(self, names: list[str]):
        if len(names) == 2:
            if type(names[0]) == type(names[1]) == str:
                data1 = self.values.filter(name=names[0].lower())
                data2 = self.values.filter(name=names[1].lower())
                dates = set(data1.values_list('date')) & set(data2.values_list('date'))
                dates = [_[0] for _ in dates]
                data1 = np.array([_[0] for _ in self.values.filter(date__in=dates, name=names[0]).values_list('value')])
                data2 = np.array([_[0] for _ in self.values.filter(date__in=dates, name=names[1]).values_list('value')])
                return np.corrcoef(data1, data2)
        raise ValueError("Unknown names data")

    def add_data(self, name: str, values: List[PydanticValue]) -> bool:
        for value in values:
            Value.objects.get_or_create(name=name.lower(), value=value.value, date=value.date, user=self)
        return True


class Value(models.Model):
    class Meta:
        verbose_name = 'Данные'
        verbose_name_plural = 'Данные'
    name = models.CharField(default='default', max_length=20, verbose_name='Имя значения')
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь', related_name='values')
    date = models.DateField(default=timezone.now, verbose_name='Дата')
    value = models.FloatField(default=0, verbose_name='Значение')
