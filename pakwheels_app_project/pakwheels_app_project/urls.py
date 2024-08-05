from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('ads/', include('ads.urls')),
    path('cars/', include('cars.urls')),
    path('users/', include('users.urls')),
    path('', include('ads.urls'))  
]
