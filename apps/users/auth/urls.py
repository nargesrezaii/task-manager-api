from django.urls import path

from apps.users.auth.views import ChangePasswordView


urlpatterns = [
    path(
        "change_password/",
        ChangePasswordView.as_view(),
        name="change-password",
    ),
]