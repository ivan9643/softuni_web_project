from django.contrib.auth import get_user_model
from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver
from softuni_web_project.accounts.models import Profile
from softuni_web_project.main_app.models import Post

UserModel = get_user_model()


@receiver(post_delete, sender=Profile)
def auto_delete_user_and_posts(sender, instance, **kwargs):
    UserModel.objects.get(id=instance.user_id).delete()
    Post.objects.filter(profile_id=instance.user_id).delete()


@receiver(post_save, sender=UserModel)
def auto_create_profile_after_creating_superuser(sender, instance, **kwargs):
    try:
        user_profile = Profile.objects.get(user_id=instance.id)
    except Profile.DoesNotExist:
        user_profile = None
    if instance.is_superuser and user_profile is None:
        superuser_profile = Profile(first_name=instance.username)
        superuser_profile.user_id = instance.id
        superuser_profile.save()
