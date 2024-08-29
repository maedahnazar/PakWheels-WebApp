from django.urls import path

from ads.api.v2.views import (
    AdListView,
    AdDetailView,
    AdRetrieveCreateView,
    UserCarsListView,
    AdRetrieveUpdateView,
    AdDeleteView,
)


urlpatterns = [
    path('', AdListView.as_view(), name='ad-list'),
    path('ad/<int:ad_id>/', AdDetailView.as_view(), name='ad-detail'),
    path('add-car/', AdRetrieveCreateView.as_view(), name='add-car'),
    path('user-cars/', UserCarsListView.as_view(), name='user-cars-list'),
    path('ad/update/<int:ad_id>/', AdRetrieveUpdateView.as_view(), name='ad-update'),
    path('car/delete/<int:ad_id>/', AdDeleteView.as_view(), name='ad-delete'),
]
