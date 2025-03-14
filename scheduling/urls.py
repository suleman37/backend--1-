from django.urls import path
from .views import schedule_interview

urlpatterns = [
    path('set/', schedule_interview, name="schedule-interview"),
]
