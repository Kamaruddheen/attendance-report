from django.urls import path
from .views import ClassesView, AttendanceView

app_name = "attendance"
urlpatterns = [
    path('', ClassesView.as_view(), name="classes"),
    path('attendance/<int:subject_id>/', AttendanceView.as_view(), name="attendance" )
]