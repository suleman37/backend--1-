from django.urls import path
from .views import conduct_ai_interview

urlpatterns = [
    path('start/', conduct_ai_interview, name="ai-interview"),
]
