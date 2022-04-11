from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from softuni_web_project.accounts.models import Profile
from softuni_web_project.main_app.models import Post


class FollowViewTests(TestCase):
    UserModel = get_user_model()
    VALID_FIRST_NAME = 'Ivan'
    VALID_LAST_NAME = 'Angelov'
    VALID_USERNAME = 'ivan'
    VALID_PASSWORD = 'my_password_123'

    def test_follow_view__following_and_redirect(self):
        user_following = self.UserModel(username=self.VALID_USERNAME)
        user_following.set_password(self.VALID_PASSWORD)
        user_following.save()
        profile_following = Profile(
            first_name=self.VALID_FIRST_NAME,
            last_name=self.VALID_LAST_NAME,
            user_id=user_following.id
        )
        profile_following.save()

        user_followed = self.UserModel(username=f'{self.VALID_USERNAME}1')
        user_followed.set_password(self.VALID_PASSWORD)
        user_followed.save()
        profile_followed = Profile(
            first_name=self.VALID_FIRST_NAME,
            last_name=self.VALID_LAST_NAME,
            user_id=user_followed.id
        )
        profile_followed.save()

        self.client.login(username=self.VALID_USERNAME, password=self.VALID_PASSWORD)
        response = self.client.get(reverse('follow', kwargs={'pk': user_followed.id}))
        self.assertTrue(profile_following in profile_followed.followers.all())
        self.assertEqual(profile_following.following.count(), 1)
        self.assertEqual(profile_followed.followers.count(), 1)
        self.assertRedirects(response, reverse('profile details', kwargs={'pk': user_followed.id}))

    def test_follow_view__unfollowing_and_redirect(self):
        user_unfollowing = self.UserModel(username=self.VALID_USERNAME)
        user_unfollowing.set_password(self.VALID_PASSWORD)
        user_unfollowing.save()
        profile_unfollowing = Profile(
            first_name=self.VALID_FIRST_NAME,
            last_name=self.VALID_LAST_NAME,
            user_id=user_unfollowing.id
        )
        profile_unfollowing.save()

        user_unfollowed = self.UserModel(username=f'{self.VALID_USERNAME}1')
        user_unfollowed.set_password(self.VALID_PASSWORD)
        user_unfollowed.save()
        profile_unfollowed = Profile(
            first_name=self.VALID_FIRST_NAME,
            last_name=self.VALID_LAST_NAME,
            user_id=user_unfollowed.id
        )
        profile_unfollowed.save()

        self.client.login(username=self.VALID_USERNAME, password=self.VALID_PASSWORD)
        self.client.get(reverse('follow', kwargs={'pk': user_unfollowed.id}))
        response = self.client.get(reverse('follow', kwargs={'pk': user_unfollowed.id}))
        self.assertFalse(profile_unfollowing in profile_unfollowed.followers.all())
        self.assertEqual(profile_unfollowing.following.count(), 0)
        self.assertEqual(profile_unfollowed.followers.count(), 0)
        self.assertRedirects(response, reverse('profile details', kwargs={'pk': user_unfollowed.id}))