from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    pass  

class Ad(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='ads')
    title = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    location = models.CharField(max_length=255)
    seller_comments = models.TextField()

    def __str__(self):
        return self.title

class Car(models.Model):
    ad = models.OneToOneField(Ad, on_delete=models.CASCADE, related_name='car')
    registered_in = models.CharField(max_length=255)
    color = models.CharField(max_length=50)
    assembly = models.CharField(max_length=50)
    engine_capacity = models.IntegerField()
    body_type = models.CharField(max_length=50)
    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.ad.title} - {self.color}"

class Feature(models.Model):
    name = models.CharField(max_length=255)
    cars = models.ManyToManyField(Car, related_name='features')

    def __str__(self):
        return self.name
    
class Source(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name
    
class InspectionReport(models.Model):
    car = models.ForeignKey(Car, on_delete=models.CASCADE, related_name='inspection_reports')
    source = models.ForeignKey(Source, on_delete=models.CASCADE, related_name='inspection_reports', default=1)  
    inspected_date = models.DateField()
    overall_rating = models.DecimalField(max_digits=3, decimal_places=2)
    grade = models.CharField(max_length=50)
    exterior_body = models.CharField(max_length=255)
    engine_transmission_clutch = models.CharField(max_length=255)
    suspension_steering = models.CharField(max_length=255)
    interior = models.CharField(max_length=255)
    ac_heater = models.CharField(max_length=255)

    def __str__(self):
        return f"Inspection Report for {self.car} on {self.inspected_date}"

class Image(models.Model):
    car = models.ForeignKey(Car, on_delete=models.CASCADE, related_name='images')
    image_url = models.URLField(blank=True, null=True)  # For images from JSON file
    image_path = models.ImageField(upload_to='car_images/', blank=True, null=True)  # For user-uploaded images

    def __str__(self):
        return f"Image for {self.car} - URL: {self.image_url}, Path: {self.image_path}"
