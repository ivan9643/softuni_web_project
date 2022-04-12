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

    def setUp(self) -> None:
        self.user_liking = self.UserModel(username=self.VALID_USERNAME)
        self.user_liking.set_password(self.VALID_PASSWORD)
        self.user_liking.save()
        self.profile_liking = Profile(
            first_name=self.VALID_FIRST_NAME,
            last_name=self.VALID_LAST_NAME,
            user=self.user_liking
        )
        self.profile_liking.save()

        self.user_with_liked_post = self.UserModel(username=f'{self.VALID_USERNAME}2')
        self.user_with_liked_post.set_password(self.VALID_PASSWORD)
        self.user_with_liked_post.save()
        self.profile_with_liked_post = Profile(
            first_name=self.VALID_FIRST_NAME,
            last_name=self.VALID_LAST_NAME,
            user=self.user_with_liked_post
        )
        self.profile_with_liked_post.save()

        self.post = Post(id=1, profile=self.profile_with_liked_post, caption=self.VALID_POST_CAPTION)
        self.post.save()

    def test_post_like_view__like_when_user_is_not_owner_of_the_post_and_redirect__ex(self):
        self.client.login(username=self.VALID_USERNAME, password=self.VALID_PASSWORD)
        response = self.client.get(reverse('post like', kwargs={'pk': self.post.id}))
        liked_post = Post.objects.get(id=self.post.id)
        self.assertEqual(liked_post.likes.count(), 1)
        self.assertTrue(self.profile_liking in liked_post.likes.all())
        self.assertRedirects(response, reverse('profile details', kwargs={'pk': self.profile_with_liked_post.user_id}))

    def test_post_like_view__unlike_when_user_is_not_owner_of_the_post_and_redirect(self):
        self.client.login(username=self.VALID_USERNAME, password=self.VALID_PASSWORD)
        self.client.get(reverse('post like', kwargs={'pk': self.post.id}))
        response = self.client.get(reverse('post like', kwargs={'pk': self.post.id}))
        unliked_post = Post.objects.get(id=self.post.id)
        self.assertEqual(unliked_post.likes.count(), 0)
        self.assertFalse(self.profile_liking in unliked_post.likes.all())
        self.assertRedirects(response, reverse('profile details', kwargs={'pk': self.profile_with_liked_post.user_id}))

    def test_post_like_view__like_when_user_is_owner_of_the_post_and_redirect(self):
        self.client.login(username=f'{self.VALID_USERNAME}2', password=self.VALID_PASSWORD)
        response = self.client.get(reverse('post like', kwargs={'pk': self.post.id}))
        liked_post = Post.objects.get(id=self.post.id)
        self.assertEqual(liked_post.likes.count(), 1)
        self.assertTrue(self.profile_with_liked_post in liked_post.likes.all())
        self.assertRedirects(response, reverse('profile details', kwargs={'pk': self.profile_with_liked_post.user_id}))

    def test_post_like_view__unlike_when_user_is_owner_of_the_post_and_redirect(self):
        self.client.login(username=f'{self.VALID_USERNAME}2', password=self.VALID_PASSWORD)
        self.client.login(username=f'{self.VALID_USERNAME}2', password=self.VALID_PASSWORD)
        self.client.get(reverse('post like', kwargs={'pk': self.post.id}))
        response = self.client.get(reverse('post like', kwargs={'pk': self.post.id}))
        unliked_post = Post.objects.get(id=self.post.id)
        self.assertEqual(unliked_post.likes.count(), 0)
        self.assertFalse(self.profile_with_liked_post in unliked_post.likes.all())
        self.assertRedirects(response, reverse('profile details', kwargs={'pk': self.profile_with_liked_post.user_id}))
