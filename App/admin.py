from django.contrib import admin
from . import models


@admin.register(models.User)
class UserModel(admin.ModelAdmin):
    pass


@admin.register(models.Value)
class ValueModel(admin.ModelAdmin):
    list_display = ('user', 'name', 'date', 'value')
