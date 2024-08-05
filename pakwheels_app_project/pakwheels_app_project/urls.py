from django.contrib import admin
from django.urls import path, include

from ads import views as ads_views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('ads/', include('ads.urls')),
    path('cars/', include('cars.urls')),
    path('users/', include('users.urls')),
    path('', ads_views.home, name='home'),  
]
