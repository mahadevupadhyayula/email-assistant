import uuid

from django.contrib.auth.models import AbstractUser
from django.db import models

from .managers import WorkspaceScopedManager


class User(AbstractUser):
    """Application identity; Gmail authorization is deliberately separate."""

    google_subject = models.CharField(max_length=255, unique=True, null=True, blank=True)


class Workspace(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=120)
    slug = models.SlugField(max_length=140, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.name


class Membership(models.Model):
    class Role(models.TextChoices):
        FOUNDER = "founder", "Founder"
        ADMIN = "admin", "Admin"
        MEMBER = "member", "Member"

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    workspace = models.ForeignKey(Workspace, on_delete=models.CASCADE, related_name="memberships")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="memberships")
    role = models.CharField(max_length=20, choices=Role.choices, default=Role.FOUNDER)
    created_at = models.DateTimeField(auto_now_add=True)

    objects = WorkspaceScopedManager()
    unscoped_objects = models.Manager()

    class Meta:
        default_manager_name = "unscoped_objects"
        constraints = [
            models.UniqueConstraint(
                fields=("workspace", "user"), name="unique_workspace_membership"
            )
        ]

    def __str__(self) -> str:
        return f"{self.user.username} in {self.workspace.name} ({self.role})"
