from django.urls import path

from .views import command_center

urlpatterns = [path("", command_center, name="command-center")]
