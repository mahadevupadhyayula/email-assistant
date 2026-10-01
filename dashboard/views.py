from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render

from accounts.services import workspace_context_for_user


@login_required
def command_center(request: HttpRequest) -> HttpResponse:
    context = workspace_context_for_user(request.user)  # type: ignore[arg-type]
    return render(
        request,
        "dashboard/command_center.html",
        {"workspace": context.workspace, "membership": context.membership},
    )
