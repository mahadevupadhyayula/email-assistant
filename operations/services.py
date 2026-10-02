from typing import Any

from accounts.models import User, Workspace

from .models import AuditEvent


def record_audit_event(
    *,
    workspace: Workspace,
    actor: User | None,
    event_type: str,
    metadata: dict[str, Any] | None = None,
) -> AuditEvent:
    return AuditEvent.unscoped_objects.create(
        workspace=workspace,
        actor=actor,
        event_type=event_type,
        metadata=metadata or {},
    )
