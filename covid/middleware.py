from django.utils import timezone
from .models import RequestLog


class RequestTimeMiddleware:

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        """
        Record start time before calling the views then record and time after
        calling the views. Save the log to database
        """
        start_time = timezone.now()

        response = self.get_response(request)
        end_time = timezone.now()
        time_stamp = round(timezone.now().timestamp())
        request_time = (end_time - start_time).total_seconds()
        log_string = f"{time_stamp}\t\t{request.path}\t\tdone in {request_time} seconds"

        RequestLog.objects.create(
            start_time=start_time,
            end_time=end_time,
            path=request.path,
            request_time=request_time,
            status_code=response.status_code,
            method = request.method,
            log=log_string
        )
        return response
