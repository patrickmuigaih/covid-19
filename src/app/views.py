from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import EstimatorSerializer
from src.estimator import estimator

@api_view(['POST'])
def estimator_view(request):
    serializer = EstimatorSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    data =  estimator(serializer.validated_data)
    
    return Response(data)
