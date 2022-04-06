from django.contrib import admin

# Register your models here.
from softuni_web_project.main_app.models import Post


@admin.register(Post)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('caption', 'photo')

