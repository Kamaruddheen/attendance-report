from django.urls import path
from .views import *
app_name='classroom'
urlpatterns=[
    path('createclass/',CreateClass,name='createclass'),
    path('editclass/<int:id>',editclass,name='editclass'),
]