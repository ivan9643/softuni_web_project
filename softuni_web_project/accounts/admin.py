from django.contrib import admin
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.utils.html import format_html
from django.utils.http import urlencode

from softuni_web_project.accounts.models import Profile
from softuni_web_project.main_app.admin import PostInlineAdmin

UserModel = get_user_model()


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'full_name')
    list_filter = ('gender',)
    inlines = (PostInlineAdmin,)


@admin.register(UserModel)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'is_staff', 'is_superuser')
    list_filter = ('is_superuser', 'is_staff')
    readonly_fields = ('last_login', 'password')

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        is_superuser = request.user.is_superuser

        if not is_superuser:
            form.base_fields['is_superuser'].disabled = True
            form.base_fields['groups'].disabled = True
            form.base_fields['user_permissions'].disabled = True

        return form
