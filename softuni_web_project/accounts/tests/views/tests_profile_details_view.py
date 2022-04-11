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

    def test_profile_details_view_context_and_template__when_user_is_owner_of_the_profile__expects_success(self):
        user = self.UserModel(username=self.VALID_USERNAME)
        user.set_password(self.VALID_PASSWORD)
        user.save()
        profile = Profile(
            first_name=self.VALID_FIRST_NAME,
            last_name=self.VALID_LAST_NAME,
            user_id=user.id
        )
        profile.save()
        post = Post(id=1,profile=profile, caption=self.VALID_POST_CAPTION)
        post.likes.add(profile)
        post.save()
        self.client.login(username=user.username, password=self.VALID_PASSWORD)
        response = self.client.get(reverse('profile details', kwargs={'pk': user.id}))
        self.assertTemplateUsed(response,'accounts/profile-details.html')
        self.assertEqual(response.context['user_profile'], profile)
        self.assertEqual(response.context['posts_count'], 1)
        self.assertEqual(response.context['likes_count'], 1)
        self.assertTrue(response.context['is_owner'])
        self.assertEqual(list(response.context['posts']), [post])
        self.assertEqual(response.context['follower_count'], 0)
        self.assertEqual(response.context['following_count'], 0)

    def test_profile_details_view_context_and_template__when_user_is_not_owner_of_the_profile__expects_success(self):
        user1 = self.UserModel(username=self.VALID_USERNAME)
        user1.set_password(self.VALID_PASSWORD)
        user1.save()
        profile1 = Profile(
            first_name=self.VALID_FIRST_NAME,
            last_name=self.VALID_LAST_NAME,
            user_id=user1.id
        )
        profile1.save()

        user2 = self.UserModel(username=f'{self.VALID_USERNAME}2')
        user2.set_password(self.VALID_PASSWORD)
        user2.save()
        profile2 = Profile(
            first_name=self.VALID_FIRST_NAME,
            last_name=self.VALID_LAST_NAME,
            user_id=user2.id
        )
        profile2.save()

        profile1.followers.add(profile2)
        profile1.following.add(profile1)
        profile2.followers.add(profile1)
        profile2.following.add(profile1)

        post = Post(id=1,profile=profile1, caption=self.VALID_POST_CAPTION)
        post.likes.add(profile1)
        post.likes.add(profile2)
        post.save()
        self.client.login(username=user2.username, password=self.VALID_PASSWORD)
        response = self.client.get(reverse('profile details', kwargs={'pk': user1.id}))
        self.assertTemplateUsed(response,'accounts/profile-details.html')
        self.assertEqual(response.context['user_profile'], profile2)
        self.assertEqual(response.context['posts_count'], 1)
        self.assertEqual(response.context['likes_count'], 2)
        self.assertFalse(response.context['is_owner'])
        self.assertEqual(list(response.context['posts']), [post])
        self.assertEqual(response.context['follower_count'], 1)
        self.assertEqual(response.context['following_count'], 1)
