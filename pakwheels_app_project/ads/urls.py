from django.urls import path

from ads.views import home, ad_detail, add_car


urlpatterns = [
    path('', home, name='home'),
    path('ad/<int:ad_id>/', ad_detail, name='ad_detail'),
    path('add-car/', add_car, name='add_car'),
]
