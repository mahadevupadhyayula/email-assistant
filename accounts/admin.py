from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import Membership, User, Workspace

admin.site.register(User, UserAdmin)
admin.site.register(Workspace)


@admin.register(Membership)
class MembershipAdmin(admin.ModelAdmin):  # type: ignore[type-arg]
    list_display = ("user", "workspace", "role", "created_at")

    def get_queryset(self, request):  # type: ignore[no-untyped-def]
        return Membership.unscoped_objects.select_related("user", "workspace")
