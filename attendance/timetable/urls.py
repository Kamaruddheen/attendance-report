from django.urls import path
from .views import *

app_name = 'timetable'

urlpatterns = [
    # Timetable Set [Create + Choose Set + Edit]
    path('<int:class_id>/set/create/',
         createtimetableset, name='createtimetableset'),
    path('<int:class_id>/set/choose/', setchoose, name='setchoose'),
    path('<int:set_id>/set/edit/', edit_set, name='edit_set'),
    # View Timetable in Set Choose
    path('showsubjects1/<int:class_id>,<int:set_id>',
         showsubjects1, name='showsubjects1'),
    # Manage Timetable
    path('<int:class_id>/manage/<int:set_id>',
         showsubjects, name='showsubjects'),
    path('<int:class_id>/create/<int:set_id>',
         createtimetable, name='createtimetable'),
    # Timetable Edit in Show Timetable
    path('edit_subjects/', edit_subjects, name='edit_subjects'),
]
