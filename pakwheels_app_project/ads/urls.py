from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name='home'),
    path('ad_list/', views.ad_list, name='ad_list'),
    path('ad/<int:ad_id>/', views.ad_detail, name='ad_detail'),
]
