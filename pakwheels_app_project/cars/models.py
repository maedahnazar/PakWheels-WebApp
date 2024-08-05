# cars/models.py
from django.db import models
from django.conf import settings

from ads.models import Ad


class Car(models.Model):
    registered_in = models.TextField()
    color = models.TextField()
    assembly = models.TextField()
    engine_capacity = models.IntegerField()
    body_type = models.TextField()
    last_updated = models.DateTimeField(auto_now=True)

    ad = models.OneToOneField(Ad, on_delete=models.CASCADE, related_name='car')

class Feature(models.Model):
    name = models.TextField()

    cars = models.ManyToManyField(Car, related_name='features')

class Source(models.Model):
    name = models.TextField()

class InspectionReport(models.Model):
    inspected_date = models.DateField(null=True, blank=True)
    overall_rating = models.TextField(null=True, blank=True)
    grade = models.TextField(null=True, blank=True)
    exterior_body = models.TextField(null=True, blank=True)
    engine_transmission_clutch = models.TextField(null=True, blank=True)
    suspension_steering = models.TextField(null=True, blank=True)
    interior = models.TextField(null=True, blank=True)
    ac_heater = models.TextField(null=True, blank=True)

    car = models.ForeignKey(Car, on_delete=models.CASCADE)
    source = models.ForeignKey(Source, on_delete=models.CASCADE)

class Image(models.Model):
    external_image_url = models.URLField(blank=True, null=True)
    uploaded_image_path = models.ImageField(upload_to='car_images/', blank=True, null=True)

    car = models.ForeignKey(Car, on_delete=models.CASCADE, related_name='images')
