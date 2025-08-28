from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import Group as BaseGroup
from .models import User, Group


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    readonly_fields = BaseUserAdmin.readonly_fields + ('api_last_ip',)

    fieldsets = BaseUserAdmin.fieldsets + (
        ('Дополнительно', {'fields': ('api_last_ip',)}),
    )


admin.site.unregister(BaseGroup)

admin.site.register(Group)
