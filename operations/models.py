import uuid

from django.conf import settings
from django.db import models

from accounts.managers import WorkspaceScopedManager
from accounts.models import Workspace


class AuditEvent(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    workspace = models.ForeignKey(Workspace, on_delete=models.CASCADE, related_name="audit_events")
    actor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name="audit_events",
    )
    event_type = models.CharField(max_length=100)
    metadata = models.JSONField(default=dict)
    created_at = models.DateTimeField(auto_now_add=True)

    objects = WorkspaceScopedManager()
    unscoped_objects = models.Manager()

    class Meta:
        default_manager_name = "unscoped_objects"
        indexes = [models.Index(fields=("workspace", "event_type", "created_at"))]
