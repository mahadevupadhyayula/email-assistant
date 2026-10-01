from dataclasses import dataclass

from django.core.exceptions import PermissionDenied

from .models import Membership, User, Workspace


@dataclass(frozen=True)
class WorkspaceContext:
    workspace: Workspace
    membership: Membership


def workspace_context_for_user(user: User) -> WorkspaceContext:
    membership = (
        Membership.unscoped_objects.select_related("workspace")
        .filter(user=user)
        .order_by("created_at")
        .first()
    )
    if membership is None:
        raise PermissionDenied("Your account is not assigned to a workspace.")
    return WorkspaceContext(workspace=membership.workspace, membership=membership)
