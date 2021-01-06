from django.urls import path
from .views import *
app_name='timetable'
urlpatterns=[
    path('createtimetable/',createtimetable,name='createtimetable'),
    path('createtimetable/<int:class_id>,<int:set_id>',createtimetable,name='createtimetable'),
    path('createtimetableset/<int:class_id>',createtimetableset,name='createtimetableset'),
    path('setchoose/<int:class_id>',setchoose,name='setchoose'),
    path('showsubjects/<int:class_id>,<int:set_id>',showsubjects,name='showsubjects'),
    path('set_info/<int:class_id>,<int:set_id>',set_info,name='set_info'),
    path('edit_subjects/<int:set_id>',edit_subjects,name='edit_subjects'),
]