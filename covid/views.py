from rest_framework.decorators import api_view, renderer_classes
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer
from .serializers import EstimatorSerializer
from src.estimator import estimator
from rest_framework_xml.renderers import XMLRenderer

@api_view(['POST'])
@renderer_classes([JSONRenderer, XMLRenderer])
def estimator_view(request, format=None):
    serializer = EstimatorSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    data =  estimator(serializer.validated_data)
    
    return Response(data)
