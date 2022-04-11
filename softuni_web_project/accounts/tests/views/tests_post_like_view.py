from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from softuni_web_project.accounts.models import Profile
from softuni_web_project.main_app.models import Post


class ProfileDetailsViewTests(TestCase):
    UserModel = get_user_model()
    VALID_FIRST_NAME = 'Ivan'
    VALID_LAST_NAME = 'Angelov'
    VALID_USERNAME = 'ivan'
    VALID_PASSWORD = 'my_password_123'
    VALID_POST_CAPTION = 'post caption'

    def test_post_like_view__like_when_user_is_not_owner_of_the_post_and_redirect(self):
        user_liking = self.UserModel(username=self.VALID_USERNAME)
        user_liking.set_password(self.VALID_PASSWORD)
        user_liking.save()
        profile_liking = Profile(
            first_name=self.VALID_FIRST_NAME,
            last_name=self.VALID_LAST_NAME,
            user_id=user_liking.id
        )
        profile_liking.save()

        user_with_liked_post = self.UserModel(username=f'{self.VALID_USERNAME}2')
        user_with_liked_post.set_password(self.VALID_PASSWORD)
        user_with_liked_post.save()
        profile_with_liked_post = Profile(
            first_name=self.VALID_FIRST_NAME,
            last_name=self.VALID_LAST_NAME,
            user_id=user_with_liked_post.id
        )
        profile_with_liked_post.save()

        post = Post(id=1, profile=profile_with_liked_post, caption=self.VALID_POST_CAPTION)
        post.save()
        self.client.login(username=self.VALID_USERNAME, password=self.VALID_PASSWORD)
        response = self.client.get(reverse('post like', kwargs={'pk': post.id}))
        liked_post = Post.objects.get(id=post.id)
        self.assertEqual(liked_post.likes.count(),1)
        self.assertTrue(profile_liking in liked_post.likes.all())
        self.assertRedirects(response, reverse('profile details', kwargs={'pk': profile_with_liked_post.user_id}))

    def test_post_like_view__unlike_when_user_is_not_owner_of_the_post_and_redirect(self):

        user_unliking = self.UserModel(username=self.VALID_USERNAME)
        user_unliking.set_password(self.VALID_PASSWORD)
        user_unliking.save()
        profile_unliking = Profile(
            first_name=self.VALID_FIRST_NAME,
            last_name=self.VALID_LAST_NAME,
            user_id=user_unliking.id
        )
        profile_unliking.save()

        user_with_unliked_post = self.UserModel(username=f'{self.VALID_USERNAME}2')
        user_with_unliked_post.set_password(self.VALID_PASSWORD)
        user_with_unliked_post.save()
        profile_with_unliked_post = Profile(
            first_name=self.VALID_FIRST_NAME,
            last_name=self.VALID_LAST_NAME,
            user_id=user_with_unliked_post.id
        )
        profile_with_unliked_post.save()

        post = Post(id=1, profile=profile_with_unliked_post, caption=self.VALID_POST_CAPTION)
        post.save()
        self.client.login(username=self.VALID_USERNAME, password=self.VALID_PASSWORD)
        self.client.get(reverse('post like', kwargs={'pk': post.id}))
        response = self.client.get(reverse('post like', kwargs={'pk': post.id}))
        unliked_post = Post.objects.get(id=post.id)
        self.assertEqual(unliked_post.likes.count(),0)
        self.assertFalse(profile_unliking in unliked_post.likes.all())
        self.assertRedirects(response, reverse('profile details', kwargs={'pk': profile_with_unliked_post.user_id}))

    def test_post_like_view__like_when_user_is_owner_of_the_post_and_redirect(self):
        user = self.UserModel(username=self.VALID_USERNAME)
        user.set_password(self.VALID_PASSWORD)
        user.save()
        profile = Profile(
            first_name=self.VALID_FIRST_NAME,
            last_name=self.VALID_LAST_NAME,
            user_id=user.id
        )
        profile.save()

        post = Post(id=1, profile=profile, caption=self.VALID_POST_CAPTION)
        post.save()
        self.client.login(username=self.VALID_USERNAME, password=self.VALID_PASSWORD)
        response = self.client.get(reverse('post like', kwargs={'pk': post.id}))
        liked_post = Post.objects.get(id=post.id)
        self.assertEqual(liked_post.likes.count(),1)
        self.assertTrue(profile in liked_post.likes.all())
        self.assertRedirects(response, reverse('profile details', kwargs={'pk': profile.user_id}))

    def test_post_like_view__unlike_when_user_is_owner_of_the_post_and_redirect(self):
        user = self.UserModel(username=self.VALID_USERNAME)
        user.set_password(self.VALID_PASSWORD)
        user.save()
        profile = Profile(
            first_name=self.VALID_FIRST_NAME,
            last_name=self.VALID_LAST_NAME,
            user_id=user.id
        )
        profile.save()

        post = Post(id=1, profile=profile, caption=self.VALID_POST_CAPTION)
        post.save()
        self.client.login(username=self.VALID_USERNAME, password=self.VALID_PASSWORD)
        self.client.get(reverse('post like', kwargs={'pk': post.id}))
        response = self.client.get(reverse('post like', kwargs={'pk': post.id}))
        unliked_post = Post.objects.get(id=post.id)
        self.assertEqual(unliked_post.likes.count(),0)
        self.assertFalse(profile in unliked_post.likes.all())
        self.assertRedirects(response, reverse('profile details', kwargs={'pk': profile.user_id}))
