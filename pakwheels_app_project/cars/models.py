from django.db import models
from django.conf import settings

from ads.models import Ad


class Car(models.Model):
    registered_in = models.TextField()
    color = models.TextField()
    assembly = models.TextField()
    engine_capacity = models.IntegerField()
    body_type = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True) 
    modified_at = models.DateTimeField(auto_now=True)

    ad = models.OneToOneField('ads.Ad', on_delete=models.CASCADE, related_name='car')

    def __str__(self):
        return (f"{self.id} - {self.body_type}, {self.engine_capacity}cc")

class Feature(models.Model):
    name = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True) 
    modified_at = models.DateTimeField(auto_now=True)

    cars = models.ManyToManyField('cars.Car', related_name='features')

    def __str__(self):
        return self.name

class Source(models.Model):
    name = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True) 
    modified_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class InspectionReport(models.Model):
    inspected_date = models.DateField(null=True, blank=True)
    overall_rating = models.TextField(null=True, blank=True)
    grade = models.TextField(null=True, blank=True)
    exterior_body = models.TextField(null=True, blank=True)
    engine_transmission_clutch = models.TextField(null=True, blank=True)
    suspension_steering = models.TextField(null=True, blank=True)
    interior = models.TextField(null=True, blank=True)
    ac_heater = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True) 
    modified_at = models.DateTimeField(auto_now=True)

    car = models.ForeignKey('cars.Car', on_delete=models.CASCADE)
    source = models.ForeignKey('cars.Source', on_delete=models.CASCADE)

    def __str__(self):
        return (f"{self.inspected_date}, {self.overall_rating}, {self.grade}")

class Image(models.Model):
    external_image_url = models.URLField(blank=True, null=True)
    uploaded_image = models.ImageField(upload_to='car_images/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True) 
    modified_at = models.DateTimeField(auto_now=True)

    car = models.ForeignKey('cars.Car', on_delete=models.CASCADE, related_name='images')

    def __str__(self):
        return (f"{self.external_image_url}, {self.uploaded_image}")
