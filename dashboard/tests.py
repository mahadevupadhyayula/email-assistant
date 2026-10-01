import pytest
from django.urls import reverse

from accounts.models import Membership, User, Workspace


@pytest.mark.django_db
def test_command_center_requires_authentication(client) -> None:  # type: ignore[no-untyped-def]
    response = client.get(reverse("command-center"))
    assert response.status_code == 302
    assert response.url.startswith(reverse("login"))


@pytest.mark.django_db
def test_founder_sees_workspace_shell(client) -> None:  # type: ignore[no-untyped-def]
    user = User.objects.create_user(username="founder", password="password")
    workspace = Workspace.objects.create(name="Acme", slug="acme")
    Membership.unscoped_objects.create(workspace=workspace, user=user)
    client.force_login(user)

    response = client.get(reverse("command-center"))

    assert response.status_code == 200
    assert b"Acme" in response.content
    assert b"No inbox items yet" in response.content
    assert b"Founder Priorities" in response.content
