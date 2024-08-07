from django.urls import path

from ads.views import home, ad_detail


urlpatterns = [
    path('', home, name='home'),
    path('ad/<int:pk>/', ad_detail, name='ad_detail'),
]
