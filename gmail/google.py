from dataclasses import dataclass
from datetime import UTC, datetime
from typing import Any

import requests
from django.conf import settings
from google.auth.exceptions import RefreshError
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import Flow

from accounts.google import client_config

GMAIL_READONLY_SCOPE = "https://www.googleapis.com/auth/gmail.readonly"
GOOGLE_EMAIL_SCOPE = "email"
GOOGLE_USERINFO_EMAIL_SCOPE = "https://www.googleapis.com/auth/userinfo.email"
GMAIL_SCOPES = ("openid", GOOGLE_EMAIL_SCOPE, GMAIL_READONLY_SCOPE)


class GmailProviderError(RuntimeError):
    """A safe provider error without token or response-body details."""


class GmailCredentialRevokedError(GmailProviderError):
    """The stored OAuth grant is permanently invalid."""


class GmailTransientProviderError(GmailProviderError):
    """The provider operation may succeed when retried."""


@dataclass(frozen=True)
class ConnectedMailbox:
    provider_account_id: str
    email_address: str
    credentials: dict[str, Any]
    scopes: tuple[str, ...]


def gmail_flow(*, redirect_uri: str, code_verifier: str | None = None) -> Flow:
    return Flow.from_client_config(
        client_config(),
        scopes=GMAIL_SCOPES,
        redirect_uri=redirect_uri,
        code_verifier=code_verifier,
        autogenerate_code_verifier=code_verifier is None,
    )


def connected_mailbox(flow: Flow) -> ConnectedMailbox:
    credentials = flow.credentials
    granted_scopes = credentials.granted_scopes
    if granted_scopes is None:
        if not credentials.has_scopes(GMAIL_SCOPES):
            raise GmailProviderError("Google did not grant the required read-only access.")
        granted_scopes = credentials.scopes
    granted = tuple(granted_scopes or ())
    granted_set = set(granted)
    allowed_scopes = {
        "openid",
        GOOGLE_EMAIL_SCOPE,
        GOOGLE_USERINFO_EMAIL_SCOPE,
        GMAIL_READONLY_SCOPE,
    }
    if (
        not {"openid", GMAIL_READONLY_SCOPE}.issubset(granted_set)
        or not {GOOGLE_EMAIL_SCOPE, GOOGLE_USERINFO_EMAIL_SCOPE}.intersection(granted_set)
        or not granted_set.issubset(allowed_scopes)
    ):
        raise GmailProviderError("Google did not grant the required read-only access.")
    response = requests.get(
        "https://gmail.googleapis.com/gmail/v1/users/me/profile",
        headers={"Authorization": f"Bearer {credentials.token}"},
        timeout=10,
    )
    if response.status_code != 200:
        raise GmailProviderError("Gmail account details could not be verified.")
    profile = response.json()
    email = str(profile.get("emailAddress", ""))
    if not email:
        raise GmailProviderError("Gmail account details were incomplete.")
    return ConnectedMailbox(
        provider_account_id=email.casefold(),
        email_address=email,
        scopes=granted,
        credentials={
            "access_token": credentials.token,
            "refresh_token": credentials.refresh_token,
            "token_uri": credentials.token_uri,
            "client_id": settings.GOOGLE_OAUTH_CLIENT_ID,
            "client_secret": settings.GOOGLE_OAUTH_CLIENT_SECRET,
            "expiry": credentials.expiry.isoformat() if credentials.expiry else None,
        },
    )


def refresh_credentials(payload: dict[str, Any]) -> dict[str, Any]:
    credentials = Credentials(  # type: ignore[no-untyped-call]
        token=payload.get("access_token"),
        refresh_token=payload.get("refresh_token"),
        token_uri=payload.get("token_uri"),
        client_id=settings.GOOGLE_OAUTH_CLIENT_ID,
        client_secret=settings.GOOGLE_OAUTH_CLIENT_SECRET,
        scopes=GMAIL_SCOPES,
    )
    try:
        from google.auth.transport.requests import Request

        credentials.refresh(Request())  # type: ignore[no-untyped-call]
    except RefreshError as exc:
        oauth_response = next((arg for arg in exc.args if isinstance(arg, dict)), {})
        if oauth_response.get("error") == "invalid_grant":
            raise GmailCredentialRevokedError("Gmail access has been revoked.") from exc
        raise GmailTransientProviderError("Gmail access could not be refreshed.") from exc
    except Exception as exc:
        raise GmailTransientProviderError("Gmail access could not be refreshed.") from exc
    return {
        **payload,
        "access_token": credentials.token,
        "expiry": credentials.expiry.astimezone(UTC).isoformat()
        if credentials.expiry
        else datetime.now(UTC).isoformat(),
    }


def revoke_credentials(payload: dict[str, Any]) -> None:
    token = payload.get("refresh_token") or payload.get("access_token")
    if not token:
        return
    try:
        response = requests.post(
            "https://oauth2.googleapis.com/revoke",
            params={"token": token},
            headers={"content-type": "application/x-www-form-urlencoded"},
            timeout=10,
        )
    except requests.RequestException as exc:
        raise GmailProviderError("Google access could not be revoked.") from exc
    if response.status_code not in (200, 400):
        raise GmailProviderError("Google access could not be revoked.")
