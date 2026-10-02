from datetime import timedelta
from typing import Any
from unittest.mock import Mock, patch

import pytest
from cryptography.fernet import Fernet
from django.urls import reverse
from django.utils import timezone
from google.auth.exceptions import RefreshError

from accounts.models import Membership, User, Workspace
from gmail.crypto import decrypt_credentials
from gmail.google import (
    GMAIL_READONLY_SCOPE,
    GMAIL_SCOPES,
    GOOGLE_USERINFO_EMAIL_SCOPE,
    ConnectedMailbox,
    GmailCredentialRevokedError,
    GmailProviderError,
    GmailTransientProviderError,
    connected_mailbox,
    refresh_credentials,
)
from gmail.models import GmailConnection
from operations.models import AuditEvent


@pytest.fixture
def founder(db: Any, client: Any) -> tuple[User, Workspace]:
    user = User.objects.create_user(username="founder@example.com", email="founder@example.com")
    workspace = Workspace.objects.create(name="Founder", slug="founder")
    Membership.unscoped_objects.create(user=user, workspace=workspace)
    client.force_login(user)
    return user, workspace


@pytest.fixture
def encryption_key(settings: Any) -> str:
    key = Fernet.generate_key().decode()
    settings.GOOGLE_TOKEN_ENCRYPTION_KEY = key
    return key


def mailbox(email: str = "founder@example.com") -> ConnectedMailbox:
    return ConnectedMailbox(
        provider_account_id=email,
        email_address=email,
        scopes=GMAIL_SCOPES,
        credentials={
            "access_token": "access-secret",
            "refresh_token": "refresh-secret",
            "token_uri": "https://oauth2.googleapis.com/token",
        },
    )


def google_credentials(
    *, granted_scopes: tuple[str, ...] | None, requested_scopes: tuple[str, ...]
) -> Mock:
    credentials = Mock()
    credentials.granted_scopes = granted_scopes
    credentials.scopes = requested_scopes
    credentials.has_scopes.return_value = set(GMAIL_SCOPES).issubset(requested_scopes)
    credentials.token = "access-secret"
    credentials.refresh_token = "refresh-secret"
    credentials.token_uri = "https://oauth2.googleapis.com/token"
    credentials.expiry = None
    return credentials


def gmail_profile_response() -> Mock:
    response = Mock(status_code=200)
    response.json.return_value = {"emailAddress": "founder@example.com"}
    return response


def test_connected_mailbox_prefers_granted_scopes_and_accepts_email_alias() -> None:
    granted = ("openid", GOOGLE_USERINFO_EMAIL_SCOPE, GMAIL_READONLY_SCOPE)
    flow = Mock(
        credentials=google_credentials(granted_scopes=granted, requested_scopes=GMAIL_SCOPES)
    )

    with patch("gmail.google.requests.get", return_value=gmail_profile_response()):
        result = connected_mailbox(flow)

    assert result.scopes == granted


def test_connected_mailbox_rejects_unapproved_granted_scope() -> None:
    granted = (*GMAIL_SCOPES, "https://www.googleapis.com/auth/gmail.modify")
    flow = Mock(
        credentials=google_credentials(granted_scopes=granted, requested_scopes=GMAIL_SCOPES)
    )

    with pytest.raises(GmailProviderError, match="required read-only access"):
        connected_mailbox(flow)


def test_connected_mailbox_falls_back_to_complete_requested_scopes() -> None:
    flow = Mock(credentials=google_credentials(granted_scopes=None, requested_scopes=GMAIL_SCOPES))

    with patch("gmail.google.requests.get", return_value=gmail_profile_response()):
        result = connected_mailbox(flow)

    assert result.scopes == GMAIL_SCOPES


def test_connected_mailbox_rejects_incomplete_requested_scope_fallback() -> None:
    requested = ("openid", "email")
    flow = Mock(credentials=google_credentials(granted_scopes=None, requested_scopes=requested))

    with pytest.raises(GmailProviderError, match="required read-only access"):
        connected_mailbox(flow)


def test_refresh_credentials_maps_invalid_grant_to_revoked_error() -> None:
    credentials = Mock()
    credentials.refresh.side_effect = RefreshError(  # type: ignore[no-untyped-call]
        "invalid_grant: Token has been revoked.", {"error": "invalid_grant"}
    )

    with (
        patch("gmail.google.Credentials", return_value=credentials),
        pytest.raises(GmailCredentialRevokedError, match="revoked"),
    ):
        refresh_credentials({"refresh_token": "refresh-secret"})


def test_refresh_credentials_maps_other_refresh_errors_to_transient() -> None:
    credentials = Mock()
    credentials.refresh.side_effect = RefreshError(  # type: ignore[no-untyped-call]
        "temporarily_unavailable", {"error": "temporarily_unavailable"}, retryable=True
    )

    with (
        patch("gmail.google.Credentials", return_value=credentials),
        pytest.raises(GmailTransientProviderError, match="could not be refreshed"),
    ):
        refresh_credentials({"refresh_token": "refresh-secret"})


@pytest.mark.django_db
def test_consent_page_is_separate_from_sign_in_and_explains_read_only_access(
    client: Any, founder: tuple[User, Workspace]
) -> None:
    response = client.get(reverse("gmail-connect"))
    assert response.status_code == 200
    assert b"Separate Gmail consent" in response.content
    assert b"cannot send, delete, archive, label" in response.content
    assert reverse("google-login").encode() not in response.content


@pytest.mark.django_db
def test_connect_requests_only_the_approved_scopes(
    client: Any, founder: tuple[User, Workspace]
) -> None:
    flow = Mock()
    flow.code_verifier = "pkce-verifier"
    flow.authorization_url.return_value = ("https://accounts.google.test/consent", "state")
    with patch("gmail.views.gmail_flow", return_value=flow) as build_flow:
        response = client.post(reverse("gmail-connect"))
    assert response.status_code == 302
    assert response.url == "https://accounts.google.test/consent"
    assert set(GMAIL_SCOPES) == {"openid", "email", GMAIL_READONLY_SCOPE}
    build_flow.assert_called_once()


@pytest.mark.django_db
def test_callback_encrypts_tokens_and_records_consent(
    client: Any, founder: tuple[User, Workspace], encryption_key: str
) -> None:
    user, workspace = founder
    session = client.session
    session["gmail_connection_oauth"] = {
        "state": "expected",
        "code_verifier": "verifier",
        "created_at": timezone.now().isoformat(),
    }
    session.save()
    flow = Mock()
    with (
        patch("gmail.views.gmail_flow", return_value=flow),
        patch("gmail.views.connected_mailbox", return_value=mailbox()),
    ):
        response = client.get(reverse("gmail-callback"), {"state": "expected", "code": "code"})

    assert response.status_code == 302
    connection = GmailConnection.objects.for_workspace(workspace).get()
    assert "access-secret" not in connection.encrypted_credentials
    assert "refresh-secret" not in connection.encrypted_credentials
    assert (
        decrypt_credentials(connection.encrypted_credentials)["refresh_token"] == "refresh-secret"
    )
    event = AuditEvent.objects.for_workspace(workspace).get(event_type="gmail.consent_granted")
    assert event.actor == user
    assert event.metadata["scopes"] == list(GMAIL_SCOPES)


@pytest.mark.django_db
def test_callback_rejects_expired_or_wrong_state_without_saving_tokens(
    client: Any, founder: tuple[User, Workspace], encryption_key: str
) -> None:
    _, workspace = founder
    session = client.session
    session["gmail_connection_oauth"] = {
        "state": "expected",
        "code_verifier": "verifier",
        "created_at": (timezone.now() - timedelta(minutes=11)).isoformat(),
    }
    session.save()
    response = client.get(reverse("gmail-callback"), {"state": "expected", "code": "code"})
    assert response.status_code == 302
    assert not GmailConnection.objects.for_workspace(workspace).exists()


@pytest.mark.django_db
def test_callback_rejects_account_mismatch(
    client: Any, founder: tuple[User, Workspace], encryption_key: str
) -> None:
    _, workspace = founder
    session = client.session
    session["gmail_connection_oauth"] = {
        "state": "expected",
        "code_verifier": "verifier",
        "created_at": timezone.now().isoformat(),
    }
    session.save()
    with (
        patch("gmail.views.gmail_flow", return_value=Mock()),
        patch("gmail.views.connected_mailbox", return_value=mailbox("other@example.com")),
    ):
        client.get(reverse("gmail-callback"), {"state": "expected", "code": "code"})
    assert not GmailConnection.objects.for_workspace(workspace).exists()


@pytest.mark.django_db
def test_disconnect_revokes_and_clears_tokens_without_deleting_connection(
    client: Any, founder: tuple[User, Workspace], encryption_key: str
) -> None:
    user, workspace = founder
    from gmail.services import connect_mailbox

    connection = connect_mailbox(workspace=workspace, actor=user, mailbox=mailbox())
    with patch("gmail.services.revoke_credentials") as revoke:
        response = client.post(reverse("gmail-disconnect"))
    assert response.status_code == 302
    connection.refresh_from_db()
    assert connection.status == GmailConnection.Status.DISCONNECTED
    assert connection.encrypted_credentials == ""
    assert connection.disconnected_at is not None
    revoke.assert_called_once()
    assert (
        AuditEvent.objects.for_workspace(workspace).filter(event_type="gmail.disconnected").exists()
    )


@pytest.mark.django_db
def test_cross_workspace_connection_cannot_be_disconnected(
    client: Any, founder: tuple[User, Workspace], encryption_key: str
) -> None:
    user, _ = founder
    other = Workspace.objects.create(name="Other", slug="other")
    from gmail.services import connect_mailbox

    connect_mailbox(workspace=other, actor=user, mailbox=mailbox("other@example.com"))
    response = client.post(reverse("gmail-disconnect"))
    assert response.status_code == 404
    assert GmailConnection.objects.for_workspace(other).get().status == "connected"


@pytest.mark.django_db
def test_active_mailbox_cannot_be_connected_to_two_workspaces(
    founder: tuple[User, Workspace], encryption_key: str
) -> None:
    from gmail.services import GmailConnectionError, connect_mailbox

    user, workspace = founder
    other = Workspace.objects.create(name="Other", slug="other")
    connect_mailbox(workspace=workspace, actor=user, mailbox=mailbox())
    with pytest.raises(GmailConnectionError, match="already connected"):
        connect_mailbox(workspace=other, actor=user, mailbox=mailbox())
    assert not GmailConnection.objects.for_workspace(other).exists()


@pytest.mark.django_db
def test_revoked_refresh_clears_credentials_and_marks_connection_expired(
    founder: tuple[User, Workspace], encryption_key: str
) -> None:
    from gmail.services import GmailConnectionError, connect_mailbox, refresh_mailbox_credentials

    user, workspace = founder
    connection = connect_mailbox(workspace=workspace, actor=user, mailbox=mailbox())
    with (
        patch(
            "gmail.services.refresh_credentials",
            side_effect=GmailCredentialRevokedError("revoked"),
        ),
        pytest.raises(GmailConnectionError, match="expired"),
    ):
        refresh_mailbox_credentials(connection)
    connection.refresh_from_db()
    assert connection.status == GmailConnection.Status.EXPIRED
    assert connection.encrypted_credentials == ""
    assert connection.last_error_code == "refresh_revoked"


@pytest.mark.django_db
def test_transient_refresh_failure_retains_credentials_and_connection(
    founder: tuple[User, Workspace], encryption_key: str
) -> None:
    from gmail.services import GmailConnectionError, connect_mailbox, refresh_mailbox_credentials

    user, workspace = founder
    connection = connect_mailbox(workspace=workspace, actor=user, mailbox=mailbox())
    encrypted_credentials = connection.encrypted_credentials
    with (
        patch(
            "gmail.services.refresh_credentials",
            side_effect=GmailTransientProviderError("temporary failure"),
        ),
        pytest.raises(GmailConnectionError, match="Please retry"),
    ):
        refresh_mailbox_credentials(connection)
    connection.refresh_from_db()
    assert connection.status == GmailConnection.Status.CONNECTED
    assert connection.encrypted_credentials == encrypted_credentials
    assert connection.last_error_code == "refresh_failed"


@pytest.mark.django_db
@pytest.mark.parametrize("status", [GmailConnection.Status.REVOKED, GmailConnection.Status.EXPIRED])
def test_unhealthy_connection_state_is_visible(
    client: Any, founder: tuple[User, Workspace], encryption_key: str, status: str
) -> None:
    _, workspace = founder
    now = timezone.now()
    GmailConnection.unscoped_objects.create(
        workspace=workspace,
        provider_account_id="founder@example.com",
        email_address="founder@example.com",
        scopes=list(GMAIL_SCOPES),
        encrypted_credentials="",
        status=status,
        consented_at=now,
        connected_at=now,
    )
    response = client.get(reverse("gmail-connection"))
    assert response.status_code == 200
    assert GmailConnection.Status(status).label.encode() in response.content


@pytest.mark.django_db
def test_expired_connection_with_credentials_can_be_revoked(
    client: Any, founder: tuple[User, Workspace], encryption_key: str
) -> None:
    user, workspace = founder
    from gmail.services import connect_mailbox

    connection = connect_mailbox(workspace=workspace, actor=user, mailbox=mailbox())
    connection.status = GmailConnection.Status.EXPIRED
    connection.save(update_fields=("status",))

    page = client.get(reverse("gmail-connection"))
    assert page.status_code == 200
    assert b"Disconnect Gmail" in page.content

    with patch("gmail.services.revoke_credentials") as revoke:
        response = client.post(reverse("gmail-disconnect"))

    assert response.status_code == 302
    connection.refresh_from_db()
    assert connection.status == GmailConnection.Status.DISCONNECTED
    assert connection.encrypted_credentials == ""
    revoke.assert_called_once()
