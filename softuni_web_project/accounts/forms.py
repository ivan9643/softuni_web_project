from django import forms
from django.contrib.auth import forms as auth_forms, get_user_model
from django.contrib.auth.forms import AuthenticationForm
from django.core.exceptions import ValidationError

from softuni_web_project.accounts.models import Profile

UserModel = get_user_model()


class RegisterForm(auth_forms.UserCreationForm):
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

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password1'].widget = forms.PasswordInput(
            attrs={
                'placeholder': 'Enter password'
            }
        )
        self.fields['password2'].widget = forms.PasswordInput(
            attrs={
                'placeholder': 'Confirm password'
            }
        )
        for field_name in ['username', 'password1', 'password2']:
            self.fields[field_name].help_text = None

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
        model = UserModel
        fields = ('username', 'password1', 'password2')
        widgets = {
            'username': forms.TextInput(
                attrs={
                    'placeholder': 'Enter username'
                }
            ),
        }


class LoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Enter username'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Enter password'}))

    def clean(self):
        username = self.cleaned_data['username']
        if not username == username.lower():
            raise ValidationError('Username must be lowercase only')


class ProfileEditForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    class Meta:
        model = Profile
        exclude = ('user', 'followers','following')
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
            ),
            'following': forms.SelectMultiple(
                attrs={
                    'size': 10,
                }
            ),
        }
