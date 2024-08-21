from django.urls import path

from ads.api.v2.views import HomeView, AdDetailView, AddCarView


urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('ad/<int:ad_id>/', AdDetailView.as_view(), name='ad-detail'),
    path('add-car/', AddCarView.as_view(), name='add-car'),
]
