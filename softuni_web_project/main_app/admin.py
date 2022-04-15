from django.contrib import admin

from softuni_web_project.main_app.admin_forms import PostInlineAdminForm
from softuni_web_project.main_app.models import Post, Hashtag


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    search_fields = ('caption', 'hashtags__name')
    list_display = ('caption', 'photo')


@admin.register(Hashtag)
class HashtagAdmin(admin.ModelAdmin):
    search_fields = ('name',)
    list_display = ('name',)


class PostInlineAdmin(admin.StackedInline):
    form = PostInlineAdminForm
    model = Post
