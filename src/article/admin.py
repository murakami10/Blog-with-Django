from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import Article
from .models import ArticleCategory
from .models import User


class UserAdminInModel(UserAdmin):
    list_display = (
        "email",
        "username",
        "first_name",
        "last_name",
        "is_staff",
        "is_active",
    )
    list_filter = (
        "email",
        "username",
        "is_staff",
        "is_active",
    )
    fieldsets = (
        (
            None,
            {"fields": ("email", "username", "first_name", "last_name", "password")},
        ),
        ("Permissions", {"fields": ("is_staff", "is_active")}),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "email",
                    "username",
                    "password1",
                    "password2",
                    "is_staff",
                    "is_active",
                ),
            },
        ),
    )
    search_fields = ("email", "username")
    ordering = ("email",)


admin.site.register(User, UserAdminInModel)
admin.site.register(Article)
admin.site.register(ArticleCategory)
