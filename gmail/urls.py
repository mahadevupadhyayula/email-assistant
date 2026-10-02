from django.urls import path

from .views import callback, connect, connection_detail, deletion_placeholder, disconnect

urlpatterns = [
    path("", connection_detail, name="gmail-connection"),
    path("connect/", connect, name="gmail-connect"),
    path("callback/", callback, name="gmail-callback"),
    path("disconnect/", disconnect, name="gmail-disconnect"),
    path("delete-data/", deletion_placeholder, name="gmail-delete-data"),
]
