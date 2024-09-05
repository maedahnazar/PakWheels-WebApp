from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path('v1/', include('ads.api.v1.urls')),
    path('v2/', include('ads.api.v2.urls')),
    path('v3/', include('ads.api.v3.urls')),
    path('v4/', include('ads.api.v4.urls')),
    path('v1/users/', include('users.api.v1.urls')),
    path('v2/users/', include('users.api.v2.urls')),
    path('v3/users/', include('users.api.v3.urls')),
    path('v4/users/', include('users.api.v4.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
