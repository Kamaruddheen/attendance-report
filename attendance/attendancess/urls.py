from django.urls import path
from .views import ClassesView

app_name = "attendance"
urlpatterns = [
    path('', ClassesView.as_view(), name="classes")
]