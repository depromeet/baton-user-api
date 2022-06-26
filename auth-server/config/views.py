from rest_framework.decorators import api_view
from rest_framework.response import Response


@api_view(['GET'])
def health(request):
    """
    health check
    """
    return Response({'message': 'baton-auth-server is healthy!'})
