from rest_framework.decorators import api_view, renderer_classes
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer
from django.http import HttpResponse
from .serializers import EstimatorSerializer
from src.estimator import estimator
from rest_framework_xml.renderers import XMLRenderer
from .models import RequestLog


@api_view(['POST'])
@renderer_classes([JSONRenderer, XMLRenderer])
def estimator_view(request, format=None):
    serializer = EstimatorSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    data =  estimator(serializer.validated_data)
    return Response(data)


@api_view(['GET'])
def logs_view(request, ):
    log_string = ''
    all_logs = RequestLog.objects.order_by('-created_on')
    for log in all_logs:
        time_stamp=  round(log.created_on.timestamp())
        log_string += f"{log.method}\t\t{log.path}\t\t{log.status_code}\t\t{log.request_time}ms\n"
    
    return HttpResponse(log_string, content_type='text/plain')
