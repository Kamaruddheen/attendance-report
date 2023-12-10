from django.urls import path

from .views import *

app_name = 'subject'

urlpatterns = [
    # path('all/', SubjectListView, name='subject_list'),
    # path('create/', SubjectCreateView, name='create_subject'),
    # path('detail/<int:id>', SubjectDetailView, name='subject_detail'),
    # path('edit/<int:id>/', SubjectEditView.as_view(), name="edit_subject"),
    # path('delete/<int:id>', SubjectDeleteView.as_view(), name="delete_subject"),

    # Create Hour & Subejcts
    path('<int:class_id>/create/', create_hour_view, name="create_hour"),
    # View Hour
    path('<int:class_id>/', HourListView, name="hour_list"),
    # View Subject
    path('<int:class_id>/hours/<int:hour_id>/subject/',
         HourDetailView, name="hour_detail"),
    # Particular Hour - Subject Edit
    path('<int:class_id>/hours/<int:hour_id>/subject/edit/',
         HourEditView, name="edit_hour"),
    # Add students for Selective Subject
    path('<int:class_id>/hours/<int:hour_id>/subject/add_students/<int:sub_id>/',
         HourAddStudView, name="hour_add_students"),
]
