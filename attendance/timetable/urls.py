from django.urls import path
from .views import *
app_name='timetable'
urlpatterns=[
    path('createtimetable/<int:id>',createtimetable,name='createtimetable')
]