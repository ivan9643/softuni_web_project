from django.contrib import admin

# Register your models here.
from softuni_web_project.main_app.forms import PostInlineAdminForm
from softuni_web_project.main_app.models import Post


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    # search_fields =
    list_display = ('caption', 'photo')


class PostInlineAdmin(admin.StackedInline):
    form = PostInlineAdminForm
    model = Post