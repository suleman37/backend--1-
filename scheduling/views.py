from rest_framework.decorators import api_view
from rest_framework.response import Response

@api_view(['POST'])
def schedule_interview(request):
    return Response({"message": "Interview scheduled"})
