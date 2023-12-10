from django.contrib import admin
from .models import *


class TimetableModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'subject', 'set_name', 'hour', 'day']
    search_fields = ['subject', 'set_name', 'hour', 'day']


admin.site.register(TimetableModel, TimetableModelAdmin)


class TimetablesetModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'classroom', 'from_date', 'to_date']
    search_fields = ['name', 'from_date', 'to_date']
    ordering = ['from_date']


admin.site.register(TimetablesetModel, TimetablesetModelAdmin)
