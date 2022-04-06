from django import forms
from django.contrib.auth import forms as auth_forms, get_user_model

from softuni_web_project.accounts.models import Profile


class CreateProfileForm(auth_forms.UserCreationForm):
    first_name = forms.CharField(
        max_length=Profile.FIRST_NAME_MAX_LENGTH,
        required=False,
    )
    last_name = forms.CharField(
        max_length=Profile.LAST_NAME_MAX_LENGTH,
        required=False,
    )
    picture = forms.ImageField(
        required=False,
    )
    date_of_birth = forms.DateField(
        required=False,
    )
    bio = forms.CharField(
        widget=forms.Textarea,
        required=False,
    )
    email = forms.EmailField(
        required=False,
    )
    gender = forms.ChoiceField(
        choices=Profile.GENDERS,
    )

    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     self._init_bootstrap_form_controls()

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
        fields = ('username', 'password1', 'password2', 'first_name', 'last_name', 'picture', 'bio')
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

        }

#
# class EditProfileForm(BootstrapFormMixin, forms.ModelForm):
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         self._init_bootstrap_form_controls()
#         self.initial['gender'] = Profile.DO_NOT_SHOW
#
#     class Meta:
#         model = Profile
#         fields = '__all__'
#         widgets = {
#             'first_name': forms.TextInput(
#                 attrs={
#                     'placeholder': 'Enter first name'
#                 }
#             ),
#             'last_name': forms.TextInput(
#                 attrs={
#                     'placeholder': 'Enter last name'
#                 }
#             ),
#             'picture': forms.TextInput(
#                 attrs={
#                     'placeholder': 'Enter URL'
#                 }
#             ),
#             'email': forms.EmailInput(
#                 attrs={
#                     'placeholder': 'Enter email'
#                 }
#             ),
#             'bio': forms.Textarea(
#                 attrs={
#                     'placeholder': 'Enter bio',
#                     'rows': 3,
#                 }
#             ),
#             'gender': forms.Select(
#                 choices=Profile.GENDERS,
#             ),
#             'date_of_birth': forms.DateInput(
#                 attrs={
#                     'min': '1920-01-01',
#                 }
#             )
#         }
#
#
# class DeleteProfileForm(forms.ModelForm):
#     def save(self, commit=True):
#         pets = list(self.instance.pet_set.all())
#         # should be done with signals
#         PetPhoto.objects.filter(tagged_pets__in=pets).delete()
#         self.instance.delete()
#         return self.instance
#
#     class Meta:
#         model = Profile
#         fields = ()
