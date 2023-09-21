from django.contrib import admin
from .models import Caller
# Register your models here.


@admin.register(Caller)
class admindata(admin.ModelAdmin):
    list_display = ['id']

