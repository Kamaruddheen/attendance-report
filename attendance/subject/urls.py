from django.urls import path

from .views import *

app_name = 'subject'

urlpatterns = [
    path('all/', SubjectListView, name='subject_list'),
    path('create/', SubjectCreateView, name='create_subject'),
    path('detail/<int:id>', SubjectDetailView, name='subject_detail'),
    path('edit/<int:id>/', SubjectEditView.as_view(), name="edit_subject"),
    path('delete/<int:id>', SubjectDeleteView.as_view(), name="delete_subject"),

    path('classroom/<int:class_id>/hour/', HourListView, name="hour_list"),
    path('classroom/<int:class_id>/hour/<int:hour_id>/', HourDetailView, name="hour_detail"),
    path('classroom/<int:class_id>/hour/<int:hour_id>/edit/', HourEditView, name="edit_hour"),
    path('classroom/<int:class_id>/hour/<int:hour_id>/add_students/<int:sub_id>/', HourAddStudView, name="hour_add_students"),
    path('classroom/<int:class_id>/hour/create/', create_hour_view, name="create_hour"),
]
