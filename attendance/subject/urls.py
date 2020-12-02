from django.urls import path

from .views import *

urlpatterns = [
	path('all/',SubjectListView,name='subject_list'),
	path('create/',SubjectCreateView,name='create_subject'),
	path('detail/<int:id>',SubjectDetailView,name='subject_detail'),
]