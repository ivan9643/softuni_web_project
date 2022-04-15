import datetime

from django import forms
from django.contrib.auth import forms as auth_forms, get_user_model
from softuni_web_project.accounts.models import Profile, Country

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
        widget=forms.SelectDateWidget(
            years=range(1920, datetime.datetime.now().year + 1)
        ),
    )
    bio = forms.CharField(
        widget=forms.Textarea(
            attrs={
                'placeholder': 'Enter bio',
                'style': 'height: 169px;'
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

    country = forms.CharField(
        required=False,
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Enter country name'
            }
        )
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.country_name = None
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

    def clean(self):
        self.country_name = self.cleaned_data['country']
        if not self.country_name.isalpha() and self.country_name:
            self.add_error('country', 'Country name must contain only letters')
        first_name = self.cleaned_data['first_name']
        last_name = self.cleaned_data['last_name']
        if len(first_name) < 2 and first_name:
            self.add_error('first_name',
                           f'Ensure this value has at least {Profile.FIRST_NAME_MIN_LENGTH} characters (it has {len(first_name)}).')
        if len(last_name) < 2 and last_name:
            self.add_error('last_name',
                           f'Ensure this value has at least {Profile.LAST_NAME_MIN_LENGTH} characters (it has {len(last_name)}).')
        if not first_name.isalpha() and first_name:
            self.add_error('first_name', 'Value must contain only letters')
        if not last_name.isalpha() and last_name:
            self.add_error('last_name', 'Value must contain only letters')
        return super().clean()

    def save(self, commit=True):
        user = super().save(commit=False)
        country = None
        try:
            country = Country.objects.get(name=self.country_name)
        except Country.DoesNotExist:
            country = Country(
                name=self.country_name
            )
            country.save()
        profile = Profile(
            first_name=self.cleaned_data['first_name'],
            last_name=self.cleaned_data['last_name'],
            picture=self.cleaned_data['picture'],
            date_of_birth=self.cleaned_data['date_of_birth'],
            bio=self.cleaned_data['bio'],
            email=self.cleaned_data['email'],
            gender=self.cleaned_data['gender'],
            user=user,
            country=country
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


class LoginForm(auth_forms.AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    username = auth_forms.UsernameField(
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Enter username'
            },
        )
    )
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs=
            {
                'placeholder': 'Enter password'
            }
        )
    )

    def clean(self):
        username = self.cleaned_data['username']
        if not username == username.lower():
            self.add_error('username', 'Username must be lowercase only')
        return super(LoginForm, self).clean()


class ChangePasswordForm(auth_forms.PasswordChangeForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.country_name = None
        self.fields['old_password'].widget = forms.PasswordInput(
            attrs={
                'placeholder': 'Enter old password'
            }
        )
        self.fields['new_password1'].widget = forms.PasswordInput(
            attrs={
                'placeholder': 'Enter new password'
            }
        )
        self.fields['new_password2'].widget = forms.PasswordInput(
            attrs={
                'placeholder': 'Confirm new password'
            }
        )
        for field_name in ['old_password', 'new_password1', 'new_password2']:
            self.fields[field_name].help_text = None


class ProfileEditForm(forms.ModelForm):
    country = forms.CharField(
        required=False,
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Enter country name'
            }
        )
    )

    gender = forms.ChoiceField(
        required=True,
        choices=Profile.GENDERS
    )

    def __init__(self, profile, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.country_name = None
        if profile.country:
            self.initial['country'] = profile.country.name

    def clean(self):
        self.country_name = self.cleaned_data['country']
        if not self.country_name.isalpha() and self.country_name:
            self.add_error('country', 'Country name must contain only letters')
        return super().clean()

    def save(self, commit=True):
        profile = super().save(commit=False)
        country = None
        try:
            country = Country.objects.get(name=self.country_name)
        except Country.DoesNotExist:
            country = Country(
                name=self.country_name
            )
            country.save()
        profile.country = country
        if commit:
            profile.save()
        return profile

    class Meta:
        model = Profile
        exclude = ('user', 'followers', 'following', 'country')
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
                    'style': 'height: 106px;',
                }
            ),
            'gender': forms.Select(
                choices=Profile.GENDERS,
            ),
            'date_of_birth': forms.SelectDateWidget(
                years=range(1920, datetime.datetime.now().year + 1),
            ),
            'following': forms.SelectMultiple(
                attrs={
                    'size': 10,
                }
            ),
        }
