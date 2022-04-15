from django import forms
from django.core.exceptions import ValidationError

from softuni_web_project.main_app.models import Post, Hashtag


class PostCreateForm(forms.ModelForm):
    def __init__(self, profile, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.profile = profile

    caption = forms.CharField(
        max_length=200,
    )

    hashtags = forms.CharField(
        required=False,
        widget=forms.Textarea(
            attrs={
                'rows': 3
            }
        )
    )

    photo = forms.ImageField(
        required=True,
    )

    def clean(self):
        hashtag_names_str = self.cleaned_data['hashtags'].lower()
        start_index = -1
        self.hashtags = []
        saved = True
        last = 0
        for i, ch in enumerate(hashtag_names_str):
            if not ch.isalpha() and not ch.isdigit() and not ch == '_' \
                    or i == len(hashtag_names_str) - 1:
                if not saved:
                    if i == len(hashtag_names_str) - 1:
                        last = 1
                    hashtag_name = hashtag_names_str[start_index:i + last]
                    if hashtag_name != '#':
                        hashtag = None
                        if len(hashtag_name) > 30:
                            self.add_error('hashtags', 'Hashtags must be maximum 30 characters long')
                            break
                        try:
                            hashtag = Hashtag.objects.get(name=hashtag_name)
                        except Hashtag.DoesNotExist:
                            hashtag = Hashtag(
                                name=hashtag_name,
                            )
                            hashtag.save()
                        self.hashtags.append(hashtag)
                    saved = True
            if ch == '#':
                start_index = i
                saved = False
        return super().clean()

    def save(self, commit=True):
        post = super().save(commit=False)
        post.profile = self.profile
        if commit:
            post.save()
            for hashtag in self.hashtags:
                post.hashtags.add(hashtag)
        return post

    class Meta:
        model = Post
        fields = ('caption', 'photo')


class PostEditForm(forms.ModelForm):
    caption = forms.CharField(
        max_length=Post.CAPTION_MAX_LENGTH,
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Enter caption'
            }
        )
    )
    hashtags = forms.CharField(
        required=False,
        widget=forms.Textarea(
            attrs={
                'rows': 3
            }
        ),
    )

    def __init__(self, post, *args, **kwargs):
        super().__init__(*args, **kwargs)
        hashtags_names = [hashtag.name for hashtag in post.hashtags.all()]
        hashtags_str = ' '.join(hashtags_names)
        self.fields['hashtags'].initial = hashtags_str

    def clean(self):
        hashtag_names_str = self.cleaned_data['hashtags'].lower()
        start_index = -1
        self.hashtags = []
        saved = True
        last = 0
        for i, ch in enumerate(hashtag_names_str):
            if not ch.isalpha() and not ch.isdigit() and not ch == '_' \
                    or i == len(hashtag_names_str) - 1:
                if not saved:
                    if i == len(hashtag_names_str) - 1:
                        last = 1
                    hashtag_name = hashtag_names_str[start_index:i + last]
                    if hashtag_name != '#':
                        hashtag = None
                        if len(hashtag_name) > 30:
                            self.add_error('hashtags', 'Hashtags must be maximum 30 characters long')
                            break
                        try:
                            hashtag = Hashtag.objects.get(name=hashtag_name)
                        except Hashtag.DoesNotExist:
                            hashtag = Hashtag(
                                name=hashtag_name,
                            )
                            hashtag.save()
                        self.hashtags.append(hashtag)
                    saved = True
            if ch == '#':
                start_index = i
                saved = False
        return super().clean()

    def save(self, commit=True):
        post = super().save(commit=False)
        if commit:
            post.save()
            post.hashtags.clear()
            for hashtag in self.hashtags:
                post.hashtags.add(hashtag)

        return post

    class Meta:
        model = Post
        fields = ('caption',)

