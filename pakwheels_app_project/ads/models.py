from django.db import models
from django.conf import settings
from django.contrib.auth import get_user_model


class Ad(models.Model):
    title = models.TextField()
    price = models.FloatField()
    location = models.TextField()
    seller_comments = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True) 
    modified_at = models.DateTimeField(auto_now=True)

    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='ads')

    def __str__(self):
        return f"{self.title} - {self.price} ({self.location})"
