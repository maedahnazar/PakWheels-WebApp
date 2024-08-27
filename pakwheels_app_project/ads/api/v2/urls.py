from django.urls import path

from ads.api.v2.views import (
    AdListView,
    AdDetailView,
    CarCreateView,
    UserCarsView,
    CarEditView,
    RemoveCarImageView,
    CarDeleteView,
)


urlpatterns = [
    path('', AdListView.as_view(), name='ad-list'),
    path('ad/<int:ad_id>/', AdDetailView.as_view(), name='ad-detail'),
    path('add-car/', CarCreateView.as_view(), name='add-car'),
    path('user-cars/', UserCarsView.as_view(), name='user-cars'),
    path('car/edit/<int:ad_id>/', CarEditView.as_view(), name='car-edit'),
    path('car/image/remove/<int:image_id>/', RemoveCarImageView.as_view(), name='remove-car-image'),
    path('car/delete/<int:ad_id>/', CarDeleteView.as_view(), name='car-delete'),
]
