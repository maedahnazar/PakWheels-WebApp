from django.urls import path

from ads.api.v1.views import ad_list_view, ad_detail_view, car_create_view


urlpatterns = [
    path('', ad_list_view, name='ad_list'),
    path('ad/<int:ad_id>/', ad_detail_view, name='ad_detail'),
    path('add-car/', car_create_view, name='add_car'),
]
