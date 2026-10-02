import secrets
from datetime import datetime, timedelta
from urllib.parse import urlsplit

from django.contrib.auth import login
from django.db import transaction
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render
from django.urls import reverse
from django.utils import timezone

from operations.services import record_audit_event

from .google import GoogleIdentityError, identity_flow, verified_identity
from .models import Membership, User, Workspace

OAUTH_SESSION_KEY = "google_identity_oauth"
STATE_LIFETIME = timedelta(minutes=10)


def _safe_next(request: HttpRequest) -> str:
    candidate = request.GET.get("next", "")
    parsed = urlsplit(candidate)
    return (
        candidate if candidate.startswith("/") and not parsed.netloc else reverse("command-center")
    )


def google_login(request: HttpRequest) -> HttpResponse:
    redirect_uri = request.build_absolute_uri(reverse("google-login-callback"))
    try:
        flow = identity_flow(redirect_uri=redirect_uri)
        authorization_url, state = flow.authorization_url(
            access_type="online",
            include_granted_scopes="false",
            prompt="select_account",
        )
    except GoogleIdentityError as exc:
        return render(request, "registration/oauth_error.html", {"message": str(exc)}, status=503)
    request.session[OAUTH_SESSION_KEY] = {
        "state": state,
        "code_verifier": flow.code_verifier,
        "next": _safe_next(request),
        "created_at": timezone.now().isoformat(),
    }
    return redirect(authorization_url)


def google_login_callback(request: HttpRequest) -> HttpResponse:
    oauth = request.session.pop(OAUTH_SESSION_KEY, None)
    if request.GET.get("error") or not oauth:
        return render(request, "registration/oauth_error.html", status=400)
    if not secrets.compare_digest(str(oauth["state"]), request.GET.get("state", "")):
        return render(request, "registration/oauth_error.html", status=400)
    try:
        created_at = datetime.fromisoformat(str(oauth["created_at"]))
        if timezone.now() - created_at > STATE_LIFETIME:
            return render(request, "registration/oauth_error.html", status=400)
    except (TypeError, ValueError):
        return render(request, "registration/oauth_error.html", status=400)
    try:
        flow = identity_flow(
            redirect_uri=request.build_absolute_uri(reverse("google-login-callback")),
            code_verifier=str(oauth["code_verifier"]),
        )
        flow.fetch_token(authorization_response=request.build_absolute_uri())
        identity = verified_identity(flow)
    except Exception:
        return render(request, "registration/oauth_error.html", status=400)

    with transaction.atomic():
        user = User.objects.filter(google_subject=identity.subject).first()
        if user is None:
            user = User.objects.filter(email__iexact=identity.email).first()
            if user is not None and user.google_subject:
                return render(request, "registration/oauth_error.html", status=409)
            if user is None:
                user = User(username=identity.email, email=identity.email)
            user.google_subject = identity.subject
            user.first_name = identity.given_name
            user.last_name = identity.family_name
            user.set_unusable_password()
            user.save()
        membership = Membership.unscoped_objects.filter(user=user).first()
        if membership is None:
            workspace = Workspace.objects.create(
                name=f"{identity.given_name or identity.email}'s Workspace",
                slug=f"workspace-{secrets.token_hex(6)}",
            )
            membership = Membership.unscoped_objects.create(workspace=workspace, user=user)
        record_audit_event(
            workspace=membership.workspace,
            actor=user,
            event_type="identity.signed_in",
            metadata={"provider": "google"},
        )
    login(request, user, backend="django.contrib.auth.backends.ModelBackend")
    return redirect(str(oauth["next"]))
