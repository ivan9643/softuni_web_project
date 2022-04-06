from django.db.models.signals import post_delete, pre_delete
from django.dispatch import receiver

from softuni_web_project.accounts.models import CustomUser, Profile


# def auto_delete_user(sender, instance, **kwargs):
#     CustomUser.objects.get(id=instance.user_id).delete()
#
#
# pre_delete.connect(auto_delete_user, sender=Profile)

#
# @receiver(post_delete, sender=CustomUser)
# def auto_delete_profile(sender, instance, **kwargs):
#     Profile.objects.get(user_id=instance.id).delete()


@receiver(post_delete, sender=Profile)
def auto_delete_user(sender, instance, **kwargs):
    CustomUser.objects.get(id=instance.user_id).delete()
