from django.urls import path, include
from users.views import register_user, login_user, logout_user

urlpatterns = [
    path("register/", register_user, name="register-user"),
    path("login/", login_user, name="login-user"),
    path("logout/", login_user, name="logout-user"),
]