from django.urls import path
from .views import *
app_name='timetable'
urlpatterns=[
    path('createtimetable/',createtimetable,name='createtimetable'),
    path('createtimetable/<int:id>',createtimetable,name='createtimetable'),
    path('createtimetableset/<int:id>',createtimetableset,name='createtimetableset'),
    path('setchoose/<int:id>',setchoose,name='setchoose'),
    path('showsubjects/<int:id>',showsubjects,name='showsubjects'),
]