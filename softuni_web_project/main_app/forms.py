from django import forms

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

    def save(self, commit=True):
        post = super().save(commit=False)
        hashtag_names_str = self.cleaned_data['hashtags'].lower()
        start_index = -1
        hashtags = []
        saved = True
        for i, ch in enumerate(hashtag_names_str):
            if i == len(hashtag_names_str) - 1:
                if not saved:
                    hashtag_name = hashtag_names_str[start_index:i + 1]
                    hashtag = None
                    try:
                        hashtag = Hashtag.objects.get(name=hashtag_name)
                    except Hashtag.DoesNotExist:
                        hashtag = Hashtag(
                            name=hashtag_name,
                        )
                        hashtag.save()
                    hashtags.append(hashtag)
            if not ch.isalpha() and not ch.isdigit() and not ch == '_':
                if not saved:
                    hashtag_name = hashtag_names_str[start_index:i]
                    if hashtag_name != '#':
                        hashtag = None
                        try:
                            hashtag = Hashtag.objects.get(name=hashtag_name)
                        except Hashtag.DoesNotExist:
                            hashtag = Hashtag(
                                name=hashtag_name,
                            )
                            hashtag.save()
                        hashtags.append(hashtag)
                    saved = True
            if ch == '#':
                start_index = i
                saved = False
        post.profile = self.profile
        if commit:
            post.save()
            for hashtag in hashtags:
                post.hashtags.add(hashtag)
        return post

    class Meta:
        model = Post
        fields = ('caption', 'photo')


class PostEditForm(forms.ModelForm):
    caption = forms.CharField(
        max_length=200,
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

    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)

        post = super().save(commit=False)
        hashtags_names = [hashtag.name for hashtag in post.hashtags.all()]
        hashtags_str = ' '.join(hashtags_names)
        self.fields['hashtags'].initial = hashtags_str

    def save(self, commit=True):
        post = super().save(commit=False)
        hashtag_names_str = self.cleaned_data['hashtags'].lower()
        start_index = -1
        hashtags = []
        saved = True
        for i, ch in enumerate(hashtag_names_str):
            if i == len(hashtag_names_str) - 1:
                if not saved:
                    hashtag_name = hashtag_names_str[start_index:i + 1]
                    hashtag = None
                    try:
                        hashtag = Hashtag.objects.get(name=hashtag_name)
                    except Hashtag.DoesNotExist:
                        hashtag = Hashtag(
                            name=hashtag_name,
                        )
                        hashtag.save()
                    hashtags.append(hashtag)
            if not ch.isalpha() and not ch.isdigit() and not ch == '_':
                if not saved:
                    hashtag_name = hashtag_names_str[start_index:i]
                    if hashtag_name != '#':
                        hashtag = None
                        try:
                            hashtag = Hashtag.objects.get(name=hashtag_name)
                        except Hashtag.DoesNotExist:
                            hashtag = Hashtag(
                                name=hashtag_name,
                            )
                            hashtag.save()
                        hashtags.append(hashtag)
                    saved = True
            if ch == '#':
                start_index = i
                saved = False
        if commit:
            post.save()
            post.hashtags.clear()
            for hashtag in hashtags:
                post.hashtags.add(hashtag)
        return post

    class Meta:
        model = Post
        fields = ('caption',)


class PostInlineAdminForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['hashtags'].required = False

    class Meta:
        model = Post
        fields = '__all__'
