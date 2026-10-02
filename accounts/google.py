from dataclasses import dataclass
from typing import Any

from django.conf import settings
from google.auth.transport.requests import Request
from google.oauth2 import id_token
from google_auth_oauthlib.flow import Flow

IDENTITY_SCOPES = ("openid", "email", "profile")


class GoogleIdentityError(RuntimeError):
    """Raised when Google identity cannot be safely established."""


@dataclass(frozen=True)
class GoogleIdentity:
    subject: str
    email: str
    given_name: str
    family_name: str


def client_config() -> dict[str, Any]:
    if not settings.GOOGLE_OAUTH_CLIENT_ID or not settings.GOOGLE_OAUTH_CLIENT_SECRET:
        raise GoogleIdentityError("Google sign-in is not configured.")
    return {
        "web": {
            "client_id": settings.GOOGLE_OAUTH_CLIENT_ID,
            "client_secret": settings.GOOGLE_OAUTH_CLIENT_SECRET,
            "auth_uri": "https://accounts.google.com/o/oauth2/auth",
            "token_uri": "https://oauth2.googleapis.com/token",
        }
    }


def identity_flow(*, redirect_uri: str, code_verifier: str | None = None) -> Flow:
    flow = Flow.from_client_config(
        client_config(),
        scopes=IDENTITY_SCOPES,
        redirect_uri=redirect_uri,
        code_verifier=code_verifier,
        autogenerate_code_verifier=code_verifier is None,
    )
    return flow


def verified_identity(flow: Flow) -> GoogleIdentity:
    raw = id_token.verify_oauth2_token(  # type: ignore[no-untyped-call]
        flow.credentials.id_token,
        Request(),
        settings.GOOGLE_OAUTH_CLIENT_ID,
    )
    if not raw.get("email_verified"):
        raise GoogleIdentityError("Google did not verify this email address.")
    subject = str(raw.get("sub", ""))
    email = str(raw.get("email", ""))
    if not subject or not email:
        raise GoogleIdentityError("Google identity response was incomplete.")
    return GoogleIdentity(
        subject=subject,
        email=email,
        given_name=str(raw.get("given_name", "")),
        family_name=str(raw.get("family_name", "")),
    )
