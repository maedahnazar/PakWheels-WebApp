from django.urls import path

from users.views import user_signup, user_login


urlpatterns = [
    path('signup/', user_signup, name='signup'),
    path('login/', user_login, name='login'),
]
