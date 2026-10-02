from django.urls import path

from .views import google_login, google_login_callback

urlpatterns = [
    path("google/login/", google_login, name="google-login"),
    path("google/callback/", google_login_callback, name="google-login-callback"),
]
