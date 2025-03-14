from django.urls import path
from .views import chatbot_response

urlpatterns = [
    path('talk/', chatbot_response, name="chatbot-response"),
]
