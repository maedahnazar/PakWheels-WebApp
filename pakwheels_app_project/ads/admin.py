from django.contrib import admin
from django.utils.html import format_html

from ads.models import Ad


@admin.register(Ad)
class AdAdmin(admin.ModelAdmin):
    list_display = ('title', 'price', 'location', 'car_id_display', 'created_at', 'modified_at')
    list_filter = ('location', 'price')

    def car_id_display(self, obj):
        return obj.car.id if obj.car else None
    
    car_id_display.short_description = 'Car ID'
    