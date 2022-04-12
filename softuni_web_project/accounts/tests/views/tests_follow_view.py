from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from softuni_web_project.accounts.models import Profile


class FollowViewTests(TestCase):
    UserModel = get_user_model()
    VALID_FIRST_NAME = 'Ivan'
    VALID_LAST_NAME = 'Angelov'
    VALID_USERNAME = 'ivan'
    VALID_PASSWORD = 'my_password_123'

    def setUp(self) -> None:
        self.user_following = self.UserModel(username=self.VALID_USERNAME)
        self.user_following.set_password(self.VALID_PASSWORD)
        self.user_following.save()
        self.profile_following = Profile(
            first_name=self.VALID_FIRST_NAME,
            last_name=self.VALID_LAST_NAME,
            user=self.user_following
        )
        self.profile_following.save()

        self.user_followed = self.UserModel(username=f'{self.VALID_USERNAME}1')
        self.user_followed.set_password(self.VALID_PASSWORD)
        self.user_followed.save()
        self.profile_followed = Profile(
            first_name=self.VALID_FIRST_NAME,
            last_name=self.VALID_LAST_NAME,
            user=self.user_followed
        )
        self.profile_followed.save()

    def test_follow_view__following_and_redirect__expect_user_to_be_followed(self):

        self.client.login(username=self.VALID_USERNAME, password=self.VALID_PASSWORD)
        response = self.client.get(reverse('follow', kwargs={'pk': self.user_followed.id}))
        self.assertTrue(self.profile_following in self.profile_followed.followers.all())
        self.assertEqual(self.profile_following.following.count(), 1)
        self.assertEqual(self.profile_followed.followers.count(), 1)
        self.assertRedirects(response, reverse('profile details', kwargs={'pk': self.user_followed.id}))

    def test_follow_view__unfollowing_and_redirect__expect_user_to_be_unfollowed(self):
        self.client.login(username=self.VALID_USERNAME, password=self.VALID_PASSWORD)
        self.client.get(reverse('follow', kwargs={'pk': self.user_followed.id}))
        response = self.client.get(reverse('follow', kwargs={'pk': self.user_followed.id}))
        self.assertFalse(self.profile_following in self.profile_followed.followers.all())
        self.assertEqual(self.profile_following.following.count(), 0)
        self.assertEqual(self.profile_followed.followers.count(), 0)
        self.assertRedirects(response, reverse('profile details', kwargs={'pk': self.user_followed.id}))