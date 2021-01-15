from django.urls import path
from .views import *
app_name='timetable'
urlpatterns=[
    path('createtimetable/<int:class_id>,<int:set_id>',createtimetable,name='createtimetable'),
    path('createtimetableset/<int:class_id>',createtimetableset,name='createtimetableset'),
    path('setchoose/<int:class_id>',setchoose,name='setchoose'),
    path('showsubjects/<int:class_id>,<int:set_id>',showsubjects,name='showsubjects'),
    path('showsubjects1/<int:class_id>,<int:set_id>',showsubjects1,name='showsubjects1'),
    path('edit_subjects/',edit_subjects,name='edit_subjects'),
]