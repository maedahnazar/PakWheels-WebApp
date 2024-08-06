from django.contrib import admin

from cars.models import Car, Feature, Image, Source, InspectionReport


@admin.register(Car)
class CarAdmin(admin.ModelAdmin):
    list_display = ('ad', 'registered_in', 'color', 'engine_capacity', 'body_type', 'created_at', 'modified_at')

@admin.register(Feature)
class FeatureAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at', 'modified_at')

@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    list_display = ('car', 'external_image_url', 'created_at', 'modified_at')

@admin.register(Source)
class SourceAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at', 'modified_at')

@admin.register(InspectionReport)
class InspectionReportAdmin(admin.ModelAdmin):
    list_display = (
        'car', 
        'source', 
        'inspected_date', 
        'overall_rating', 
        'grade', 
        'exterior_body', 
        'engine_transmission_clutch', 
        'suspension_steering', 
        'interior', 
        'ac_heater', 
        'created_at', 
        'modified_at'
    )
