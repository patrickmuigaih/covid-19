from django.db import models

class RequestLog(models.Model):
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    path = models.CharField(max_length=100)
    request_time = models.IntegerField()