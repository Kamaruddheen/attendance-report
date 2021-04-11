from django.contrib import admin
from .models import AttendanceIdModel, AttendanceModel


class AttendanceIdModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'date', 'hour_fk',
                    'subject', 'hour', 'classroom', 'status']
    search_fields = ['date', 'subject']


class AttendanceModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'attendance_id', 'rollno', 'status']


admin.site.register(AttendanceIdModel, AttendanceIdModelAdmin)
admin.site.register(AttendanceModel, AttendanceModelAdmin)
