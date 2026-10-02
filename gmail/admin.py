from django.contrib import admin

from .models import GmailConnection


@admin.register(GmailConnection)
class GmailConnectionAdmin(admin.ModelAdmin):  # type: ignore[type-arg]
    list_display = ("email_address", "workspace", "status", "updated_at")
    readonly_fields = (
        "encrypted_credentials",
        "provider_account_id",
        "scopes",
        "consented_at",
        "connected_at",
    )

    def get_queryset(self, request):  # type: ignore[no-untyped-def]
        return GmailConnection.unscoped_objects.select_related("workspace")
