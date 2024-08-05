from django.urls import path

from ads.views import home, display_ads, ad_detail


urlpatterns = [
    path('', home, name='home'),
    path('display_ads/', display_ads, name='display_ads'),
    path('ad/<int:ad_id>/', ad_detail, name='ad_detail'),
]
