from django.contrib import admin
from .models import Servio


@admin.register(Servio)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['url_main', 'updated']
