from django.urls import path
from users.views import UserRegistrationAPIView, UserLoginAPIView, UserLogoutAPIView

urlpatterns = [
    path("api/register/", UserRegistrationAPIView.as_view(), name="register-user"),
    path("api/login/", UserLoginAPIView.as_view(), name="login-user"),
    path("api/logout/", UserLogoutAPIView.as_view(), name="logout-user"),
]