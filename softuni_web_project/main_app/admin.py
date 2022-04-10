from django.contrib import admin

# Register your models here.
from softuni_web_project.main_app.models import Post


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('caption', 'photo')


class PostInlineAdmin(admin.StackedInline):
    model = Post
