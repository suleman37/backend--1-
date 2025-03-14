from rest_framework.decorators import api_view
from rest_framework.response import Response

@api_view(['POST'])
def conduct_ai_interview(request):
    return Response({"message": "AI interview started"})
