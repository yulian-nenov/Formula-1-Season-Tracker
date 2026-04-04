from django.contrib.auth import get_user_model
from django.contrib.auth.models import User, Group
from django.db.models.signals import post_save
from django.dispatch import receiver

from accounts.models import Profile

UserModel = get_user_model()

@receiver(post_save, sender=UserModel)
def create_profile_and_add_to_user_group(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(pk=instance.pk)
        group, _ = Group.objects.get_or_create(name='Users')
        instance.groups.add(group)
