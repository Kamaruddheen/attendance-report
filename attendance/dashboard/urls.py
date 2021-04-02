from django.urls import path
from .views import *

app_name = 'dashboard'

urlpatterns = [
    path('', dashboard_view, name="view"),
]
