from django.urls import path
from .views import *

app_name = 'classroom'

urlpatterns = [
    path('createclass/', CreateClass, name='createclass'),
    path('editclass/<int:id>/', editclass, name='editclass'),
    path('<int:id>/students/', ManageStudents, name='manage_students'), #get request will list all students and post request will delete particular student
    path('<int:id>/students/add/', AddStudents, name='add_students'),
    path('students/update/', ajax_update_student, name='update_student'),
]
