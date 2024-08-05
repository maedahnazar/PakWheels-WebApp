from django.db import models
from django.conf import settings


class Ad(models.Model):
    title = models.TextField()
    price = models.FloatField()
    location = models.TextField()
    seller_comments = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True) 
    last_updated = models.DateTimeField(auto_now=True)

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='ads')
