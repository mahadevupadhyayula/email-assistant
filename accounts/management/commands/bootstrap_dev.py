from django.conf import settings
from django.core.management.base import BaseCommand, CommandError

from accounts.models import Membership, User, Workspace


class Command(BaseCommand):
    help = "Idempotently create the local founder account and workspace."

    def add_arguments(self, parser) -> None:  # type: ignore[no-untyped-def]
        parser.add_argument("--username", default="founder")
        parser.add_argument("--password", default="local-founder")
        parser.add_argument("--workspace", default="Founder Workspace")

    def handle(self, *args: object, **options: object) -> None:
        if not settings.DEBUG:
            raise CommandError("bootstrap_dev is available only when DEBUG is enabled")

        username = str(options["username"])
        password = str(options["password"])
        workspace_name = str(options["workspace"])
        user, _ = User.objects.get_or_create(username=username)
        user.set_password(password)
        user.save(update_fields=("password",))
        workspace, _ = Workspace.objects.get_or_create(
            slug="founder-workspace", defaults={"name": workspace_name}
        )
        Membership.unscoped_objects.get_or_create(
            user=user,
            workspace=workspace,
            defaults={"role": Membership.Role.FOUNDER},
        )
        self.stdout.write(self.style.SUCCESS(f"Development account ready: {username}"))
