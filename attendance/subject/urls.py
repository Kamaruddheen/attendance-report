from django.urls import path

from .views import *

app_name = 'subject'

urlpatterns = [
    path('all/', SubjectListView, name='subject_list'),
    path('create/', SubjectCreateView, name='create_subject'),
    path('detail/<int:id>', SubjectDetailView, name='subject_detail'),
    path('edit/<int:id>/', SubjectEditView.as_view(), name="edit_subject"),
    path('delete/<int:id>', SubjectDeleteView.as_view(), name="delete_subject")
]
