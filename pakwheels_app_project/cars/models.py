from django.db import models

from core.mixins import TimestampMixin  


class Car(TimestampMixin):
    registered_in = models.TextField()
    color = models.TextField()
    assembly = models.TextField()
    engine_capacity = models.IntegerField()
    body_type = models.TextField()

    ad = models.OneToOneField('ads.Ad', on_delete=models.CASCADE, related_name='car')

    def __str__(self):
        return f"{self.id} - {self.body_type} | {self.engine_capacity}cc"

class Feature(TimestampMixin):
    name = models.TextField()

    cars = models.ManyToManyField('cars.Car', related_name='features', through='CarFeature')

    def __str__(self):
        return self.name
    
class CarFeature(TimestampMixin):
    car = models.ForeignKey('cars.Car', on_delete=models.CASCADE, related_name='car_features')
    feature = models.ForeignKey('cars.Feature', on_delete=models.CASCADE, related_name='car_features')

class Source(TimestampMixin):
    name = models.TextField()

    def __str__(self):
        return self.name

class InspectionReport(TimestampMixin):
    inspected_date = models.DateField(null=True, blank=True)
    overall_rating = models.TextField(null=True, blank=True)
    grade = models.TextField(null=True, blank=True)
    exterior_body = models.TextField(null=True, blank=True)
    engine_transmission_clutch = models.TextField(null=True, blank=True)
    suspension_steering = models.TextField(null=True, blank=True)
    interior = models.TextField(null=True, blank=True)
    ac_heater = models.TextField(null=True, blank=True)

    car = models.ForeignKey('cars.Car', on_delete=models.CASCADE, related_name='inspection_reports')
    source = models.ForeignKey('cars.Source', on_delete=models.CASCADE, related_name='inspection_reports')

    def __str__(self):
        return (f"{self.inspected_date}, {self.overall_rating}, {self.grade}")

class Image(TimestampMixin):
    external_image_url = models.URLField(blank=True, null=True)
    uploaded_image = models.ImageField(upload_to='car_images/', blank=True, null=True)

    car = models.ForeignKey('cars.Car', on_delete=models.CASCADE, related_name='images')

    def __str__(self):
        return (f"{self.external_image_url}, {self.uploaded_image}")
