from django.contrib import admin
from .models import AttendanceIdModel, AttendanceModel, DayOrderModel, LeaveDateModel


class AttendanceIdModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'date', 'hour_fk',
                    'subject', 'hour', 'classroom', 'status']
    search_fields = ['date', 'subject']


class AttendanceModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'attendance_id', 'rollno', 'status']


@admin.register(DayOrderModel)
class DayOrderModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'date', 'order']
    search_fields = ['date', 'order']


@admin.register(LeaveDateModel)
class LeaveDateModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'leave_date', 'name', ]
    search_fields = ['leave_date', 'name']


admin.site.register(AttendanceIdModel, AttendanceIdModelAdmin)
admin.site.register(AttendanceModel, AttendanceModelAdmin)
# admin.site.register(DayOrderModel, DayOrderModelAdmin)
# admin.site.register(LeaveDateModel, LeaveDateModelAdmin)
