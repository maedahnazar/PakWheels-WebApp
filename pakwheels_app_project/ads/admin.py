from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from ads.models import Ad


class PriceRangeFilter(admin.SimpleListFilter):
    title = _('price range')
    parameter_name = 'price_range'

    def lookups(self, request, model_admin):
        return (
            ('0-5', _('0 - 5')),
            ('5-10', _('5 - 10')),
            ('10-20', _('10 - 20')),
            ('20-50', _('20 - 50')),
            ('50+', _('50+')),
        )

    def queryset(self, request, queryset):
        value = self.value()
        if not value:
            return queryset

        if value == '50+':
            return queryset.filter(price__gte=50)
        
        if '-' in value:
            min_price, max_price = map(int, value.split('-'))
            return queryset.filter(price__gte=min_price, price__lte=max_price)
        
        return queryset

@admin.register(Ad)
class AdAdmin(admin.ModelAdmin):
    list_display = ('title', 'price', 'location', 'car_id_display', 'created_at', 'modified_at')
    list_filter = (PriceRangeFilter, 'location')  # Add custom filter here

    def car_id_display(self, obj):
        return obj.car.id if obj.car else None
    
    car_id_display.short_description = 'Car ID'
