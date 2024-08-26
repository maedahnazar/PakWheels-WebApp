import django_filters
from django.forms import TextInput, NumberInput

from ads.models import Ad


class AdFilter(django_filters.FilterSet):
    title = django_filters.CharFilter(
        field_name='title',
        lookup_expr='icontains',
        widget=TextInput(attrs={'placeholder': 'Filter by title'})
    )
    location = django_filters.CharFilter(
        field_name='location',
        lookup_expr='icontains',
        widget=TextInput(attrs={'placeholder': 'Filter by location'})
    )
    min_price = django_filters.NumberFilter(
        field_name='price',
        lookup_expr='gte',
        widget=NumberInput(attrs={'placeholder': 'Min Price'})
    )
    max_price = django_filters.NumberFilter(
        field_name='price',
        lookup_expr='lte',
        widget=NumberInput(attrs={'placeholder': 'Max Price'})
    )

    class Meta:
        model = Ad
        fields = ['title', 'location', 'min_price', 'max_price']
