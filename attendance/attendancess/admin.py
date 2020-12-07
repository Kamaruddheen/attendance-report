from django.contrib import admin
from .models import AttendanceIdModel, AttendanceModel


class AttendanceIdModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'date', 'subject', 'status', 'handled_by']
    search_fields = ['date', 'subject', 'handled_by']

class AttendanceModelAdmin(admin.ModelAdmin):
    list_display = ['attendance_id', 'rollno', 'status']


admin.site.register(AttendanceIdModel, AttendanceIdModelAdmin)
admin.site.register(AttendanceModel, AttendanceModelAdmin)
