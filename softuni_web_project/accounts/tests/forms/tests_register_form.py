from django.contrib.auth import get_user_model
from django.test import TestCase
from softuni_web_project.accounts.forms import RegisterForm
from softuni_web_project.accounts.models import Profile


class RegisterFormTests(TestCase):
    UserModel = get_user_model()
    VALID_FIRST_NAME = 'Ivan'
    VALID_LAST_NAME = 'Angelov'
    VALID_USERNAME = 'ivan'
    VALID_PASSWORD = 'my_password_123'
    VALID_GENDER = 'Do not show'

    def test_register__when_information_is_valid__expect_success_and_created_user_and_profile(self):
        data = {
            'username': self.VALID_USERNAME,
            'password1': self.VALID_PASSWORD,
            'password2': self.VALID_PASSWORD,
            'first_name': self.VALID_FIRST_NAME,
            'last_name': self.VALID_LAST_NAME,
            'gender': self.VALID_GENDER,
        }
        form = RegisterForm(data)
        self.assertTrue(form.is_valid())
        form.save()
        user = self.UserModel.objects.get(username=self.VALID_USERNAME)
        profile = Profile.objects.get(user=user)
        self.assertIsNotNone(user)
        self.assertIsNotNone(profile)
