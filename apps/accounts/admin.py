from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _

from . models import User

class UserAdmin(BaseUserAdmin):
    list_display = ('first_name', 'last_name', 'email', 'is_email_verified', 'created_at')

    list_filter = list_display
    ordering = ["first_name","last_name", "email" ]
    fieldsets=(
        (
            _('Login Credientials'), 
            {'fields': ('email', 'password')}
        ),
        (
            _('Personal Information'),
            {'fields':('first_name', "last_name", 'avatar')}
        ),
        (
            _("Permissions & Groups"),
            {"fields":("is_email_verified", "is_profile_complete", "is_active", "is_staff", "is_superuser" ,"groups","user_permissions")}
        ),
        (
            _('Important Dates'),
            {"fields":("created_at", "updated_at", "last_login" )}
        )

    )

    add_fieldsets = (
       ( 
           None,
        {
            "classes": ('wide',),
            'fields': (
                'first_name',
                "last_name",
                "email",
                "password1",
                "password2",
                "is_staff",
                "is_superuser",
                "is_active"
            ),
          },
        ),
    )

    readonly_fields = ('created_at', 'updated_at')

admin.site.register(User, UserAdmin)

