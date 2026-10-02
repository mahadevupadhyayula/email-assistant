from dataclasses import dataclass

from django.db import IntegrityError, transaction
from django.utils import timezone

from accounts.models import User, Workspace
from operations.services import record_audit_event

from .crypto import decrypt_credentials, encrypt_credentials
from .google import (
    ConnectedMailbox,
    GmailCredentialRevokedError,
    GmailProviderError,
    refresh_credentials,
    revoke_credentials,
)
from .models import GmailConnection


class GmailConnectionError(RuntimeError):
    """A connection lifecycle error safe to show to the founder."""


@dataclass(frozen=True)
class DisconnectResult:
    provider_revoked: bool


def refresh_mailbox_credentials(connection: GmailConnection) -> GmailConnection:
    if connection.status != GmailConnection.Status.CONNECTED:
        raise GmailConnectionError("This Gmail connection is not active.")
    try:
        refreshed = refresh_credentials(decrypt_credentials(connection.encrypted_credentials))
    except GmailCredentialRevokedError as exc:
        connection.status = GmailConnection.Status.EXPIRED
        connection.encrypted_credentials = ""
        connection.last_error_code = "refresh_revoked"
        connection.last_checked_at = timezone.now()
        connection.save(
            update_fields=(
                "status",
                "encrypted_credentials",
                "last_error_code",
                "last_checked_at",
                "updated_at",
            )
        )
        raise GmailConnectionError("Gmail access expired. Reconnect to continue.") from exc
    except GmailProviderError as exc:
        connection.last_error_code = "refresh_failed"
        connection.last_checked_at = timezone.now()
        connection.save(update_fields=("last_error_code", "last_checked_at", "updated_at"))
        raise GmailConnectionError("Gmail access could not be refreshed. Please retry.") from exc
    now = timezone.now()
    connection.encrypted_credentials = encrypt_credentials(refreshed)
    connection.token_refreshed_at = now
    connection.last_checked_at = now
    connection.last_error_code = ""
    connection.save(
        update_fields=(
            "encrypted_credentials",
            "token_refreshed_at",
            "last_checked_at",
            "last_error_code",
            "updated_at",
        )
    )
    return connection


def connect_mailbox(
    *, workspace: Workspace, actor: User, mailbox: ConnectedMailbox
) -> GmailConnection:
    if not mailbox.credentials.get("refresh_token"):
        raise GmailConnectionError("Google did not return renewable Gmail access. Please retry.")
    now = timezone.now()
    try:
        with transaction.atomic():
            connection = (
                GmailConnection.unscoped_objects.select_for_update()
                .filter(workspace=workspace)
                .first()
            )
            if connection is None:
                connection = GmailConnection(workspace=workspace)
            connection.provider_account_id = mailbox.provider_account_id
            connection.email_address = mailbox.email_address
            connection.scopes = list(mailbox.scopes)
            connection.encrypted_credentials = encrypt_credentials(mailbox.credentials)
            connection.status = GmailConnection.Status.CONNECTED
            connection.consented_at = now
            connection.connected_at = now
            connection.disconnected_at = None
            connection.last_error_code = ""
            connection.save()
            record_audit_event(
                workspace=workspace,
                actor=actor,
                event_type="gmail.consent_granted",
                metadata={"scopes": list(mailbox.scopes)},
            )
    except IntegrityError as exc:
        raise GmailConnectionError(
            "That Gmail account is already connected to a workspace."
        ) from exc
    return connection


def disconnect_mailbox(
    *, workspace: Workspace, actor: User, connection: GmailConnection
) -> DisconnectResult:
    if connection.workspace_id != workspace.id:
        raise GmailConnectionError("This Gmail connection does not belong to your workspace.")
    provider_revoked = True
    try:
        revoke_credentials(decrypt_credentials(connection.encrypted_credentials))
    except Exception:
        provider_revoked = False
    connection.status = GmailConnection.Status.DISCONNECTED
    connection.disconnected_at = timezone.now()
    connection.encrypted_credentials = ""
    connection.last_error_code = "provider_revoke_failed" if not provider_revoked else ""
    connection.save(
        update_fields=(
            "status",
            "disconnected_at",
            "encrypted_credentials",
            "last_error_code",
            "updated_at",
        )
    )
    record_audit_event(
        workspace=workspace,
        actor=actor,
        event_type="gmail.disconnected",
        metadata={"provider_revoked": provider_revoked},
    )
    return DisconnectResult(provider_revoked=provider_revoked)
