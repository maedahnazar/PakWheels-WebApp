from django.contrib import admin
from .models import User, Ad, Car, Feature, InspectionReport, Image, Source


admin.site.register(User)
admin.site.register(Ad)
admin.site.register(Car)
admin.site.register(Feature)
admin.site.register(InspectionReport)
admin.site.register(Image)
admin.site.register(Source)
