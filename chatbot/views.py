from rest_framework.decorators import api_view
from rest_framework.response import Response

@api_view(['POST'])
def chatbot_response(request):
    return Response({"message": "Chatbot response"})
