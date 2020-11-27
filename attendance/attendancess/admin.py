from django.contrib import admin
from .models import AttendanceModel


class AttendanceModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'date', 'subject', 'status', 'handled_by']
    search_fields = ['date', 'subject', 'handled_by']


admin.site.register(AttendanceModel, AttendanceModelAdmin)
