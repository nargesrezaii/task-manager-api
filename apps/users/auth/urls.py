from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from apps.users.auth.views import (
    ChangePasswordView,
    LoginView,
    UserRegistrationView,
    MeView,
    LogoutView,
)


urlpatterns = [
    path(
        "change_password/",
        ChangePasswordView.as_view(),
        name="change-password",
    ),
    path(
        "register/",
        UserRegistrationView.as_view(),
        name="register",
    ),
    path(
        "login/",
        LoginView.as_view(),
        name="login",
    ),
    path(
        "me/",
        MeView.as_view(),
        name="me",
    ),
    path(
        "refresh/",
        TokenRefreshView.as_view(),
        name="refresh",
    ),
    path(
        'logout/',
        LogoutView.as_view(),
        name='logout'
    ),
]