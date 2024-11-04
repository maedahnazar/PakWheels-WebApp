from django.urls import path

from users.api.v4.views import LoginView, SignupView


urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('signup/', SignupView.as_view(), name='signup'),
]
