import pytest
from django.db import IntegrityError

from accounts.managers import WorkspaceScopeRequired
from accounts.models import Membership, User, Workspace
from accounts.services import workspace_context_for_user


@pytest.mark.django_db
def test_membership_requires_workspace_scope() -> None:
    with pytest.raises(WorkspaceScopeRequired):
        Membership.objects.all()


@pytest.mark.django_db
def test_membership_scope_cannot_cross_workspaces() -> None:
    user = User.objects.create_user(username="founder")
    first = Workspace.objects.create(name="First", slug="first")
    second = Workspace.objects.create(name="Second", slug="second")
    Membership.unscoped_objects.create(workspace=first, user=user)
    Membership.unscoped_objects.create(workspace=second, user=user, role=Membership.Role.MEMBER)

    first_memberships = Membership.objects.for_workspace(first)
    second_memberships = Membership.objects.for_workspace(second)
    assert list(first_memberships.values_list("workspace_id", flat=True)) == [first.id]
    assert list(second_memberships.values_list("workspace_id", flat=True)) == [second.id]


@pytest.mark.django_db(transaction=True)
def test_user_can_have_only_one_membership_per_workspace() -> None:
    user = User.objects.create_user(username="founder")
    workspace = Workspace.objects.create(name="First", slug="first")
    Membership.unscoped_objects.create(workspace=workspace, user=user)
    with pytest.raises(IntegrityError):
        Membership.unscoped_objects.create(workspace=workspace, user=user)


@pytest.mark.django_db
def test_workspace_context_is_explicit() -> None:
    user = User.objects.create_user(username="founder")
    workspace = Workspace.objects.create(name="First", slug="first")
    Membership.unscoped_objects.create(workspace=workspace, user=user)

    assert workspace_context_for_user(user).workspace == workspace
