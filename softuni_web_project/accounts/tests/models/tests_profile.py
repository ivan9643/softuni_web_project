from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.test import TestCase

from softuni_web_project.accounts.models import Profile


class ProfileTests(TestCase):
    UserModel = get_user_model()
    VALID_FIRST_NAME = 'Ivan'
    VALID_LAST_NAME = 'Angelov'
    VALID_USERNAME = 'ivan'
    VALID_PASSWORD = 'my_password_123'

    def test_profile_create__when_first_name_contains_only_letters__expect_success(self):
        user = self.UserModel(username=self.VALID_USERNAME, password=self.VALID_PASSWORD)
        user.save()
        profile = Profile(
            first_name=self.VALID_FIRST_NAME,
            last_name=self.VALID_LAST_NAME,
            user_id=user.id,
        )
        profile.save()

    def test_profile_create__when_first_name_contains_a_digit__expect_fail(self):
        user = self.UserModel(username=self.VALID_USERNAME, password=self.VALID_PASSWORD)
        user.save()
        profile = Profile(
            first_name=f'{self.VALID_FIRST_NAME}2',
            last_name=self.VALID_LAST_NAME,
            user_id=user.id,
        )

        with self.assertRaises(ValidationError) as context:
            profile.full_clean()
            profile.save()

        self.assertIsNotNone(context.exception)

    def test_profile_create__when_first_name_contains_a_space__expect_fail(self):
        user = self.UserModel(username=self.VALID_USERNAME, password=self.VALID_PASSWORD)
        user.save()
        profile = Profile(
            first_name=f'{self.VALID_FIRST_NAME} ',
            last_name=self.VALID_LAST_NAME,
            user_id=user.id,
        )

        with self.assertRaises(ValidationError) as context:
            profile.full_clean()
            profile.save()

        self.assertIsNotNone(context.exception)

    def test_profile_full_name__when_valid__expect_correct_full_name(self):
        profile = Profile(
            first_name=self.VALID_FIRST_NAME,
            last_name=self.VALID_LAST_NAME
        )

        self.assertEqual(f'{self.VALID_FIRST_NAME} {self.VALID_LAST_NAME}', profile.full_name)
