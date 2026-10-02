import uuid

from django.db import models

from accounts.managers import WorkspaceScopedManager
from accounts.models import Workspace


class GmailConnection(models.Model):
    class Status(models.TextChoices):
        CONNECTED = "connected", "Connected"
        DISCONNECTED = "disconnected", "Disconnected"
        REVOKED = "revoked", "Access revoked"
        EXPIRED = "expired", "Credentials expired"
        ERROR = "error", "Needs attention"

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    workspace = models.OneToOneField(
        Workspace, on_delete=models.CASCADE, related_name="gmail_connection"
    )
    provider_account_id = models.CharField(max_length=255)
    email_address = models.EmailField()
    scopes = models.JSONField(default=list)
    encrypted_credentials = models.TextField()
    status = models.CharField(max_length=20, choices=Status.choices)
    consented_at = models.DateTimeField()
    connected_at = models.DateTimeField()
    disconnected_at = models.DateTimeField(null=True, blank=True)
    token_refreshed_at = models.DateTimeField(null=True, blank=True)
    last_checked_at = models.DateTimeField(null=True, blank=True)
    last_error_code = models.CharField(max_length=50, blank=True)
    history_id = models.CharField(max_length=255, blank=True)
    sync_page_token = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = WorkspaceScopedManager()
    unscoped_objects = models.Manager()

    class Meta:
        default_manager_name = "unscoped_objects"
        constraints = [
            models.UniqueConstraint(
                fields=("provider_account_id",),
                condition=models.Q(status="connected"),
                name="unique_active_gmail_provider_account",
            )
        ]
