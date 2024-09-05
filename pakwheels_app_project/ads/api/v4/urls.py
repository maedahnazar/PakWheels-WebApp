from django.urls import path
from ads.api.v4.views import (
    AdListView, AdDetailView, AdCreateView, AdUpdateView, AdDeleteView, UserCarsListView
)

urlpatterns = [
    path('ads/', AdListView.as_view(), name='ad-list'),
    path('ads/<int:ad_id>/', AdDetailView.as_view(), name='ad-detail'),
    path('create/ad/', AdCreateView.as_view(), name='ad-create'),
    path('update/ad/<int:ad_id>/', AdUpdateView.as_view(), name='ad-update'),
    path('delete/ad/<int:ad_id>/', AdDeleteView.as_view(), name='ad-delete'),
    path('user/cars/', UserCarsListView.as_view(), name='user-cars-list'),
]
