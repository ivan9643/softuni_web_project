from django.contrib import admin

from softuni_web_project.accounts.models import Profile, CustomUser


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name')


@admin.register(CustomUser)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('username',)
