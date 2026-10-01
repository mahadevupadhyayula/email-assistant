import pytest
from django.core.management import call_command
from django.core.management.base import CommandError

from accounts.models import Membership, User, Workspace


@pytest.mark.django_db
def test_bootstrap_dev_is_idempotent(settings) -> None:  # type: ignore[no-untyped-def]
    settings.DEBUG = True
    call_command("bootstrap_dev", username="founder", password="secret")
    call_command("bootstrap_dev", username="founder", password="secret")

    assert User.objects.filter(username="founder").count() == 1
    assert Workspace.objects.filter(slug="founder-workspace").count() == 1
    assert Membership.unscoped_objects.count() == 1


@pytest.mark.django_db
def test_bootstrap_dev_is_disabled_outside_debug(settings) -> None:  # type: ignore[no-untyped-def]
    settings.DEBUG = False
    with pytest.raises(CommandError, match="only when DEBUG is enabled"):
        call_command("bootstrap_dev")
