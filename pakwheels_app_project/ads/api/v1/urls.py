from django.urls import path

from ads.api.v1.views import (
    ad_list_view, 
    ad_detail_view, 
    car_create_view, 
    user_cars_view, 
    car_edit_view, 
    car_delete_view, 
    remove_car_image_view
)


urlpatterns = [
    path('', ad_list_view, name='ad_list'),
    path('ad/<int:ad_id>/', ad_detail_view, name='ad_detail'),
    path('add-car/', car_create_view, name='add_car'),
    path('my-cars/', user_cars_view, name='user_cars'),
    path('car/edit/<int:ad_id>/', car_edit_view, name='car_edit'),
    path('car/delete/<int:ad_id>/', car_delete_view, name='car_delete'),
    path('remove-image/<int:image_id>/', remove_car_image_view, name='remove_car_image'),
]
