from django.urls import path

from ads.api.v1.views import ad_list, ad_detail, create_car


urlpatterns = [
    path('', ad_list, name='ad_list'),
    path('ad/<int:ad_id>/', ad_detail, name='ad_detail'),
    path('add-car/', create_car, name='add_car'),
]
