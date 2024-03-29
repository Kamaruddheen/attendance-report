from django.urls import path
from .views import *

app_name = 'dashboard'

urlpatterns = [
    path('', dashboard_view, name="view"),
    path('all/', all_data, name='all_data'),
    path('student/', student_details, name="student_roll_no"),
    path('attendance_classwise/', attendance_classwise,
         name='attendance_classwise'),
    path('attendance_calender/', all_day_calender,
         name='attendance_calender'),
]
