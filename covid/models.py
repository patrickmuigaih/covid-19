from django.db import models
from django.utils.timezone import now

class RequestLog(models.Model):
    created_on = models.DateTimeField(auto_now_add=now)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    path = models.CharField(max_length=100)
    request_time = models.IntegerField()
    log = models.TextField()