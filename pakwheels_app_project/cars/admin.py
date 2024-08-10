from django.contrib import admin

from cars.models import Car, Feature, InspectionReport, Source


@admin.register(Car)
class CarAdmin(admin.ModelAdmin):
    list_display = (
        'id', 
        'registered_in', 
        'color', 
        'assembly', 
        'engine_capacity', 
        'body_type', 
        'ad_id_display', 
        'created_at', 
        'modified_at'
    )
    
    list_filter = ('registered_in', 'color', 'assembly', 'engine_capacity', 'body_type', 'ad', 'features')

    def ad_id_display(self, obj):
        return obj.ad.id if obj.ad else None
    
    ad_id_display.short_description = 'Ad ID'

@admin.register(Feature)
class FeatureAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'created_at', 'modified_at')
    list_filter = ('name',)

@admin.register(InspectionReport)
class InspectionReportAdmin(admin.ModelAdmin):
    list_display = (
        'id', 
        'inspected_date', 
        'overall_rating', 
        'grade', 
        'exterior_body', 
        'engine_transmission_clutch', 
        'suspension_steering', 
        'interior', 
        'ac_heater', 
        'car_id_display', 
        'source_id_display', 
        'created_at', 
        'modified_at'
    )

    list_filter = (
        'inspected_date', 
        'overall_rating', 
        'grade', 
        'exterior_body', 
        'engine_transmission_clutch', 
        'suspension_steering', 
        'interior', 
        'ac_heater'
    )
    
    def car_id_display(self, obj):
        return obj.car.id if obj.car else None
    
    car_id_display.short_description = 'Car ID'

    def source_id_display(self, obj):
        return getattr(obj.source, 'id', None) if hasattr(obj, 'source') else None

    source_id_display.short_description = 'Source ID'

@admin.register(Source)
class SourceAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'created_at', 'modified_at')
