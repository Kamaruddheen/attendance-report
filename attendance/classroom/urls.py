from django.urls import path
from .views import *

app_name = 'classroom'

urlpatterns = [
    path('', CreateClass, name='createclass'),
    path('manage/<int:id>/', editclass, name='editclass'),
    # get request will list all students and post request will delete particular student
    path('students/<int:id>/', ManageStudents, name='manage_students'),
    path('students/<int:id>/add/', AddStudents, name='add_students'),
    path('students/<int:id>/update/', ajax_update_student, name='update_student'),
]
