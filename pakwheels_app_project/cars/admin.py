from django.contrib import admin

from .models import Car, Feature, Source, InspectionReport, Image


admin.site.register(Car)
admin.site.register(Feature)
admin.site.register(Source)
admin.site.register(InspectionReport)
admin.site.register(Image)
