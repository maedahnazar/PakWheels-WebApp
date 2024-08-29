from django.urls import path

from ads.api.v1.views import (
    ad_list_view, 
    ad_detail_view, 
    ad_create_view, 
    user_cars_list_view, 
    ad_update_view, 
    ad_delete_view, 
)


urlpatterns = [
    path('', ad_list_view, name='ad_list'),
    path('ad/<int:ad_id>/', ad_detail_view, name='ad_detail'),
    path('add-car/', ad_create_view, name='add_car'),
    path('user-cars/', user_cars_list_view, name='user_cars_list'),
    path('ad/update/<int:ad_id>/', ad_update_view, name='ad_update'),
    path('ad/delete/<int:ad_id>/', ad_delete_view, name='ad_delete'),
]
