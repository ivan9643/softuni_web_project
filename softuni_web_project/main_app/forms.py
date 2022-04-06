from django import forms

from softuni_web_project.main_app.models import Post


class CreatePostForm(forms.ModelForm):
    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = user

    caption = forms.CharField(
        max_length=200,
    )

    photo = forms.ImageField(
        required=False,
    )

    def save(self, commit=True):
        post = super().save(commit=False)
        post.user = self.user
        if commit:
            post.save()
        return post
    # hashtags = forms.
    # make hashtags in post.save method
    #     def save(self, commit=True):
    #         user = super().save(commit=False)
    #         profile = Profile(
    #             first_name=self.cleaned_data['first_name'],
    #             last_name=self.cleaned_data['last_name'],
    #             picture=self.cleaned_data['picture'],
    #             date_of_birth=self.cleaned_data['date_of_birth'],
    #             bio=self.cleaned_data['bio'],
    #             email=self.cleaned_data['email'],
    #             gender=self.cleaned_data['gender'],
    #             user=user
    #         )
    #         user.save()
    #         if commit:
    #             profile.save()
    #         return user

    class Meta:
        model = Post
        fields = ('caption', 'photo')
