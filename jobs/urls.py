from django.urls import path
from .views import JobListCreateViewz

urlpatterns = [
    path('', JobListCreateView.as_view(), name='job-list'),
]