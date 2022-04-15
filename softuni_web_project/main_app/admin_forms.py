from django import forms
from softuni_web_project.main_app.models import Post


class PostInlineAdminForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['hashtags'].required = False

    class Meta:
        model = Post
        fields = '__all__'
