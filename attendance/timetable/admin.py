from django.contrib import admin
from .models import TimetableModel

# Register your models here.
# admin.site.register(TimetableModel)


class TimetableModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'classroom', 'sub', 'set_name', 'hour', 'day']
    search_fields = ['set_name', 'hour', 'day']


admin.site.register(TimetableModel, TimetableModelAdmin)
