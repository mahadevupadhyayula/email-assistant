import secrets
from datetime import datetime, timedelta
from typing import cast

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import Http404, HttpRequest, HttpResponse
from django.shortcuts import redirect, render
from django.urls import reverse
from django.utils import timezone

from accounts.models import User
from accounts.services import workspace_context_for_user

from .google import GmailProviderError, connected_mailbox, gmail_flow
from .models import GmailConnection
from .services import GmailConnectionError, connect_mailbox, disconnect_mailbox

OAUTH_SESSION_KEY = "gmail_connection_oauth"
STATE_LIFETIME = timedelta(minutes=10)


def _connection_for_request(request: HttpRequest) -> GmailConnection | None:
    context = workspace_context_for_user(request.user)  # type: ignore[arg-type]
    return GmailConnection.objects.for_workspace(context.workspace).first()


@login_required
def connection_detail(request: HttpRequest) -> HttpResponse:
    context = workspace_context_for_user(request.user)  # type: ignore[arg-type]
    return render(
        request,
        "gmail/connection_detail.html",
        {"workspace": context.workspace, "connection": _connection_for_request(request)},
    )


@login_required
def connect(request: HttpRequest) -> HttpResponse:
    if request.method == "POST":
        redirect_uri = request.build_absolute_uri(reverse("gmail-callback"))
        try:
            flow = gmail_flow(redirect_uri=redirect_uri)
            authorization_url, state = flow.authorization_url(
                access_type="offline",
                include_granted_scopes="false",
                prompt="consent select_account",
            )
        except Exception:
            messages.error(request, "Google connection is not configured.")
            return redirect("gmail-connection")
        request.session[OAUTH_SESSION_KEY] = {
            "state": state,
            "code_verifier": flow.code_verifier,
            "created_at": timezone.now().isoformat(),
        }
        return redirect(authorization_url)
    return render(request, "gmail/consent.html")


@login_required
def callback(request: HttpRequest) -> HttpResponse:
    oauth = request.session.pop(OAUTH_SESSION_KEY, None)
    if request.GET.get("error"):
        messages.error(request, "Gmail access was not granted. Your inbox remains disconnected.")
        return redirect("gmail-connection")
    if not oauth or not secrets.compare_digest(str(oauth["state"]), request.GET.get("state", "")):
        messages.error(request, "The Gmail connection request expired or could not be verified.")
        return redirect("gmail-connection")
    created_at = datetime.fromisoformat(str(oauth["created_at"]))
    if timezone.now() - created_at > STATE_LIFETIME:
        messages.error(request, "The Gmail connection request expired. Please start again.")
        return redirect("gmail-connection")
    try:
        flow = gmail_flow(
            redirect_uri=request.build_absolute_uri(reverse("gmail-callback")),
            code_verifier=str(oauth["code_verifier"]),
        )
        flow.fetch_token(authorization_response=request.build_absolute_uri())
        mailbox = connected_mailbox(flow)
        user = cast(User, request.user)
        signed_in_email = user.email.casefold()
        if signed_in_email and mailbox.email_address.casefold() != signed_in_email:
            raise GmailConnectionError("Connect the same Google account used to sign in.")
        context = workspace_context_for_user(user)
        connect_mailbox(
            workspace=context.workspace,
            actor=user,
            mailbox=mailbox,
        )
    except (GmailProviderError, GmailConnectionError) as exc:
        messages.error(request, str(exc))
    except Exception:
        messages.error(request, "Gmail could not be connected. No credentials were saved.")
    else:
        messages.success(request, "Gmail connected with read-only access.")
    return redirect("gmail-connection")


@login_required
def disconnect(request: HttpRequest) -> HttpResponse:
    if request.method != "POST":
        raise Http404
    context = workspace_context_for_user(request.user)  # type: ignore[arg-type]
    connection = (
        GmailConnection.objects.for_workspace(context.workspace)
        .filter(encrypted_credentials__gt="")
        .first()
    )
    if connection is None:
        raise Http404
    actor = cast(User, request.user)
    result = disconnect_mailbox(
        workspace=context.workspace,
        actor=actor,
        connection=connection,
    )
    if result.provider_revoked:
        messages.success(request, "Gmail disconnected. Stored inbox data was not deleted.")
    else:
        messages.warning(
            request,
            "Disconnected locally, but Google revocation could not be confirmed. "
            "Review Google account access.",
        )
    return redirect("gmail-connection")


@login_required
def deletion_placeholder(request: HttpRequest) -> HttpResponse:
    return render(request, "gmail/deletion_placeholder.html")
