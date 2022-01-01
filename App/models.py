from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User as DjangoUser


class User(models.Model):
    name = models.CharField()
    user = models.ForeignKey(DjangoUser, on_delete=models.CASCADE, verbose_name='Пользователь', related_name='info')

    def get_correlation(self):
        pass


class Value(models.Model):
    name = models.CharField(default='default', max_length=20, verbose_name='Имя значения')
    user = models.ForeignKey(User, on_delete='Пользователь', related_name='values')
    date = models.DateField(default=timezone.now, verbose_name='Дата')
    value = models.FloatField(default=0, verbose_name='Значение')
