from unittest.mock import Mock, patch

import pytest
from django.urls import reverse
from django.utils import timezone

from accounts.google import IDENTITY_SCOPES, GoogleIdentity
from accounts.models import Membership, User
from operations.models import AuditEvent


@pytest.mark.django_db
def test_google_sign_in_uses_identity_scopes_not_gmail(client, settings) -> None:  # type: ignore[no-untyped-def]
    settings.GOOGLE_OAUTH_CLIENT_ID = "client"
    settings.GOOGLE_OAUTH_CLIENT_SECRET = "secret"
    flow = Mock()
    flow.code_verifier = "verifier"
    flow.authorization_url.return_value = ("https://accounts.google.test/login", "state")
    with patch("accounts.views.identity_flow", return_value=flow):
        response = client.get(reverse("google-login"))
    assert response.status_code == 302
    assert set(IDENTITY_SCOPES) == {"openid", "email", "profile"}
    assert "gmail" not in " ".join(IDENTITY_SCOPES)


@pytest.mark.django_db
def test_google_callback_creates_workspace_and_audits_sign_in(client) -> None:  # type: ignore[no-untyped-def]
    session = client.session
    session["google_identity_oauth"] = {
        "state": "expected",
        "code_verifier": "verifier",
        "next": "/",
        "created_at": timezone.now().isoformat(),
    }
    session.save()
    identity = GoogleIdentity("google-123", "founder@example.com", "Maya", "Founder")
    with (
        patch("accounts.views.identity_flow", return_value=Mock()),
        patch("accounts.views.verified_identity", return_value=identity),
    ):
        response = client.get(
            reverse("google-login-callback"), {"state": "expected", "code": "code"}
        )
    assert response.status_code == 302
    user = User.objects.get(google_subject="google-123")
    membership = Membership.unscoped_objects.get(user=user)
    assert (
        AuditEvent.objects.for_workspace(membership.workspace)
        .filter(event_type="identity.signed_in")
        .exists()
    )


@pytest.mark.django_db
def test_google_callback_rejects_invalid_state(client) -> None:  # type: ignore[no-untyped-def]
    session = client.session
    session["google_identity_oauth"] = {
        "state": "expected",
        "code_verifier": "verifier",
        "next": "/",
        "created_at": timezone.now().isoformat(),
    }
    session.save()
    response = client.get(reverse("google-login-callback"), {"state": "wrong", "code": "code"})
    assert response.status_code == 400
    assert User.objects.count() == 0


@pytest.mark.django_db
def test_google_callback_rejects_malformed_session_timestamp(client) -> None:  # type: ignore[no-untyped-def]
    session = client.session
    session["google_identity_oauth"] = {
        "state": "expected",
        "code_verifier": "verifier",
        "next": "/",
        "created_at": "not-a-timestamp",
    }
    session.save()

    response = client.get(reverse("google-login-callback"), {"state": "expected", "code": "code"})

    assert response.status_code == 400
    assert User.objects.count() == 0
