from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from softuni_web_project.accounts.models import Profile


class SearchProfileViewTests(TestCase):
    UserModel = get_user_model()
    VALID_FIRST_NAME = 'Ivan'
    VALID_LAST_NAME = 'Angelov'
    VALID_USERNAME = 'ivan'
    VALID_PASSWORD = 'my_password_123'

    def test_search_profile_view_context_and_template_with_not_authenticated_user__expect_success(self):
        user = self.UserModel(username=self.VALID_USERNAME)
        user.set_password(self.VALID_PASSWORD)
        user.save()
        profile = Profile(
            first_name=self.VALID_FIRST_NAME,
            last_name=self.VALID_LAST_NAME,
            user=user
        )
        profile.save()
        response = self.client.get(reverse('search profiles'), data=
        {
            'search_text_input': self.VALID_USERNAME
        })
        list_expected = [profile]
        list_actual = list(response.context['profiles'])

        self.assertEqual(list_actual,list_expected)
        self.assertTemplateUsed(response,'main_app/search-profiles.html')