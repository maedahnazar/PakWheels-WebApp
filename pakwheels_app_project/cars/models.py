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

    def __str__(self):
        return (f"Color: {self.color} Body Type: {self.body_type} Engine Capacity{self.engine_capacity}cc"
                f"Assembly{self.assembly}, Registered in {self.registered_in}, Ad: {self.ad.title}")

class Feature(models.Model):
    name = models.TextField()

    cars = models.ManyToManyField(Car, related_name='features')

    def __str__(self):
            return f"Feature: {self.name}"

class Source(models.Model):
    name = models.TextField()

    def __str__(self):
        return f"Source: {self.name}"

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

    def __str__(self):
        return (f"Inspection Report for {self.car.color} {self.car.body_type} "
                f"({self.inspected_date}) - Source: {self.source.name}, "
                f"Rating: {self.overall_rating}, Grade: {self.grade}")

class Image(models.Model):
    external_image_url = models.URLField(blank=True, null=True)
    uploaded_image = models.ImageField(upload_to='car_images/', blank=True, null=True)

    car = models.ForeignKey(Car, on_delete=models.CASCADE, related_name='images')

    def __str__(self):
        return (f"Image for {self.car.color} {self.car.body_type} - "
                f"URL: {self.external_image_url}, Path: {self.uploaded_image}")
