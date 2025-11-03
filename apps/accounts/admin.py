from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _

from .forms import CustomUser, CustomUserChangeForm, CustomUserCreationForm
from .models import OneTimePassword, PasswordResetCode, Profile


class UserAdmin(BaseUserAdmin):
    ordering = ["-date_joined"]
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    list_display = [
        "pkid",
        "id",
        "email",
        "auth_provider",
        "first_name",
        "last_name",
        "is_staff",
        "is_active",
        "date_joined",
    ]
    list_display_links = ["id", "email"]
    list_filter = [
        "email",
        "auth_provider",
        "first_name",
        "last_name",
        "is_staff",
        "is_active",
    ]
    fieldsets = (
        (
            _("Login Credentials"),
            {"fields": ("email", "password")},
        ),
        (
            _("Personal Information"),
            {"fields": ("first_name", "last_name")},
        ),
        (
            _("Permissions and Groups"),
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                )
            },
        ),
        (_("Important Dates"), {"fields": ("last_login", "date_joined")}),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("email", "password1", "password2", "is_staff", "is_active"),
            },
        ),
    )
    search_fields = ["email", "first_name", "last_name"]


class ProfileAdmin(admin.ModelAdmin):
    ordering = ["-user"]
    list_display = ["id", "user", "phone_number", "city", "gender"]
    list_display_links = ["id", "user"]
    list_filter = ["gender", "city"]

    def get_form(self, request, obj=None, **kwargs):
        form = super(ProfileAdmin, self).get_form(request, obj, **kwargs)
        form.base_fields["preferred_locations"].required = False
        return form


admin.site.register(Profile, ProfileAdmin)
admin.site.register(CustomUser, UserAdmin)
admin.site.register([OneTimePassword, PasswordResetCode])
