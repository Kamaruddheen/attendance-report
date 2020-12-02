from django.urls import path
from .views import AttendanceView

app_name = "attendance"
urlpatterns = [
    path('', AttendanceView.as_view(), name="attendance")
]