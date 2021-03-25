from django.urls import path
from .views import ClassesView, AttendanceView, CheckAttendanceView

app_name = 'attendancess'

urlpatterns = [
    path('', ClassesView.as_view(), name="classes"),
    path('attendance/<int:hour_id>/<int:hour_number>', AttendanceView.as_view(), name="attendance" ),
    path('ViewAttendance/', CheckAttendanceView.as_view(), name="check-attendance")
]