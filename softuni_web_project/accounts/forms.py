from django import forms
from django.contrib.auth import forms as auth_forms, get_user_model

from softuni_web_project.accounts.models import Profile, CustomUser
from softuni_web_project.main_app.models import Post


class CreateProfileForm(auth_forms.UserCreationForm):
    first_name = forms.CharField(
        max_length=Profile.FIRST_NAME_MAX_LENGTH,
        required=False,
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Enter first name'
            }
        )
    )
    last_name = forms.CharField(
        max_length=Profile.LAST_NAME_MAX_LENGTH,
        required=False,
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Enter last name'
            }
        )
    )
    picture = forms.ImageField(
        required=False,
    )
    date_of_birth = forms.DateField(
        required=False,
        widget=forms.DateInput(
            attrs={
                'placeholder': 'Enter date of birth'
            }
        )
    )
    bio = forms.CharField(
        widget=forms.Textarea(
            attrs={
                'placeholder': 'Enter bio',
                'rows': 5,
            }
        ),
        required=False,
    )
    email = forms.EmailField(
        required=False,
        widget=forms.EmailInput(
            attrs={
                'placeholder': 'Enter email'
            }
        )
    )
    gender = forms.ChoiceField(
        choices=Profile.GENDERS,
        initial='Do not show',
    )

    def save(self, commit=True):
        user = super().save(commit=False)
        profile = Profile(
            first_name=self.cleaned_data['first_name'],
            last_name=self.cleaned_data['last_name'],
            picture=self.cleaned_data['picture'],
            date_of_birth=self.cleaned_data['date_of_birth'],
            bio=self.cleaned_data['bio'],
            email=self.cleaned_data['email'],
            gender=self.cleaned_data['gender'],
            user=user
        )
        user.save()
        if commit:
            profile.save()
        return user

    class Meta:
        model = get_user_model()
        fields = ('username', 'password1', 'password2')
        widgets = {
            'username': forms.TextInput(
                attrs={
                    'placeholder': 'Enter username'
                }
            ),
        }


class ProfileEditForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.initial['gender'] = Profile.DO_NOT_SHOW

    class Meta:
        model = Profile
        # fields = ('first_name','last_name','picture','date_of_birth','bio','email','gender')
        exclude = ('user',)
        widgets = {
            'first_name': forms.TextInput(
                attrs={
                    'placeholder': 'Enter first name'
                }
            ),
            'last_name': forms.TextInput(
                attrs={
                    'placeholder': 'Enter last name'
                }
            ),
            # 'picture': forms.TextInput(
            #     attrs={
            #         'placeholder': 'Enter URL'
            #     }
            # ),
            'email': forms.EmailInput(
                attrs={
                    'placeholder': 'Enter email'
                }
            ),
            'bio': forms.Textarea(
                attrs={
                    'placeholder': 'Enter bio',
                    'rows': 5,
                }
            ),
            'gender': forms.Select(
                choices=Profile.GENDERS,
            ),
            'date_of_birth': forms.DateInput(
                attrs={
                    # 'min': '1920-01-01',
                }
            )
        }


# class ProfileDeleteForm(forms.ModelForm):
#     # def save(self, commit=True):
#     #     # should be done with signals
#     #     Post.objects.filter(user_id=self.instance.user_id).delete()
#     #     CustomUser.objects.get(id=self.instance.user_id).delete()
#     #     self.instance.delete()
#     #     return self.instance
#
#
#     class Meta:
#         model = Profile
#         fields = ()
