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
        self.user1 = self.UserModel(username=self.VALID_USERNAME)
        self.user1.set_password(self.VALID_PASSWORD)
        self.user1.save()
        self.profile1 = Profile(
            first_name=self.VALID_FIRST_NAME,
            last_name=self.VALID_LAST_NAME,
            user=self.user1
        )
        self.profile1.save()
        self.post = Post(id=1,profile=self.profile1, caption=self.VALID_POST_CAPTION)
        self.post.save()


    def test_profile_details_view_context_and_template__when_user_is_owner_of_the_profile__expect_success(self):
        self.post.likes.add(self.profile1)
        self.client.login(username=self.user1.username, password=self.VALID_PASSWORD)
        response = self.client.get(reverse('profile details', kwargs={'pk': self.user1.id}))
        self.assertTemplateUsed(response,'accounts/profile-details.html')
        self.assertEqual(response.context['user_profile'], self.profile1)
        self.assertEqual(response.context['posts_count'], 1)
        self.assertEqual(response.context['likes_count'], 1)
        self.assertTrue(response.context['is_owner'])
        self.assertEqual(list(response.context['posts']), [self.post])
        self.assertEqual(response.context['follower_count'], 0)
        self.assertEqual(response.context['following_count'], 0)

    def test_profile_details_view_context_and_template__when_user_is_not_owner_of_the_profile__expect_success(self):
        user2 = self.UserModel(username=f'{self.VALID_USERNAME}2')
        user2.set_password(self.VALID_PASSWORD)
        user2.save()
        profile2 = Profile(
            first_name=self.VALID_FIRST_NAME,
            last_name=self.VALID_LAST_NAME,
            user_id=user2.id
        )
        profile2.save()

        self.profile1.followers.add(profile2)
        self.profile1.following.add(self.profile1)
        profile2.followers.add(self.profile1)
        profile2.following.add(self.profile1)

        self.post.likes.add(self.profile1)
        self.post.likes.add(profile2)
        self.client.login(username=user2.username, password=self.VALID_PASSWORD)
        response = self.client.get(reverse('profile details', kwargs={'pk': self.user1.id}))
        self.assertTemplateUsed(response,'accounts/profile-details.html')
        self.assertEqual(response.context['user_profile'], profile2)
        self.assertEqual(response.context['posts_count'], 1)
        self.assertEqual(response.context['likes_count'], 2)
        self.assertFalse(response.context['is_owner'])
        self.assertEqual(list(response.context['posts']), [self.post])
        self.assertEqual(response.context['follower_count'], 1)
        self.assertEqual(response.context['following_count'], 1)
