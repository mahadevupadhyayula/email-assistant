from typing import Any, TypeVar

from django.db import models

ScopedModel = TypeVar("ScopedModel", bound=models.Model)


class WorkspaceScopeRequired(RuntimeError):
    """Raised when tenant data is accessed without an explicit workspace."""


class WorkspaceScopedManager(models.Manager[ScopedModel]):
    """A manager that only exposes records after a workspace is supplied."""

    def get_queryset(self) -> models.QuerySet[ScopedModel]:
        raise WorkspaceScopeRequired(
            f"{self.model.__name__} queries require .for_workspace(workspace)"
        )

    def for_workspace(self, workspace: Any) -> models.QuerySet[ScopedModel]:
        workspace_id = getattr(workspace, "pk", workspace)
        if workspace_id is None:
            raise WorkspaceScopeRequired("A persisted workspace is required")
        return super().get_queryset().filter(workspace_id=workspace_id)
