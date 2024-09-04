from django.urls import path

from ads.api.v3.views import ad_list_view, ad_detail_view, ad_create_view, user_cars_list_view, ad_update_view, ad_delete_view


urlpatterns = [
    path('ads/', ad_list_view, name='ad-list'),
    path('ads/<int:ad_id>/', ad_detail_view, name='ad_detail'),
    path('create/ad/', ad_create_view, name='create-ad'),
    path('update/ad/<int:ad_id>/', ad_update_view, name='ad_update'),
    path('delete/ad/<int:ad_id>/', ad_delete_view, name='ad_delete'),
    path('user/ads/', user_cars_list_view, name='user_cars_list'),
]
