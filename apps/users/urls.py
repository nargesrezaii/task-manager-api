from django.urls import include, path

from apps.users.views import MeView, UserRegistrationView


urlpatterns = [
    path('me/', MeView.as_view(), name="me"),
    path('register/', UserRegistrationView.as_view(), name="register"),
]
