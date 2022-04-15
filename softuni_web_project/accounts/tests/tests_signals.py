from django.contrib.auth import get_user_model
from django.test import TestCase
from softuni_web_project.accounts.models import Profile
from softuni_web_project.main_app.models import Post


class SignalsTests(TestCase):
    UserModel = get_user_model()
    VALID_FIRST_NAME = 'Ivan'
    VALID_LAST_NAME = 'Angelov'
    VALID_USERNAME = 'ivan'
    VALID_PASSWORD = 'my_password_123'
    VALID_POST_CAPTION = 'post caption'

    def setUp(self) -> None:
        self.user = self.UserModel(username=self.VALID_USERNAME)
        self.user.set_password(self.VALID_PASSWORD)
        self.user.is_superuser = True
        self.user.save()

    def test_auto_create_profile_after_creating_superuser(self):
        try:
            user_profile = Profile.objects.get(user=self.user)
        except Profile.DoesNotExist:
            user_profile = None
        self.assertIsNotNone(user_profile)

    def test_auto_delete_user_and_posts(self):
        profile = Profile(
            first_name=self.VALID_FIRST_NAME,
            last_name=self.VALID_LAST_NAME,
            user=self.user
        )
        profile.save()
        post = Post(id=1, profile=profile, caption=self.VALID_POST_CAPTION)
        post.likes.add(profile)
        post.save()
        profile.delete()
        try:
            user = self.UserModel.objects.get(id=self.user.id)
        except self.UserModel.DoesNotExist:
            user = None
        try:
            post = Post.objects.get(profile_id=profile.user_id)
        except Post.DoesNotExist:
            post = None
        self.assertIsNone(user)
        self.assertIsNone(post)
