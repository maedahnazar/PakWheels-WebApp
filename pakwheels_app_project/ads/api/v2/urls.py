from django.urls import path

from ads.api.v2.views import AdListView, AdDetailView, CreateCarView


urlpatterns = [
    path('', AdListView.as_view(), name='ad-list'),
    path('ad/<int:ad_id>/', AdDetailView.as_view(), name='ad-detail'),
    path('add-car/', CreateCarView.as_view(), name='add-car'),
]
