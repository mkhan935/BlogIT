from django.db.models.signals import post_save
from django.dispatch import receiver

from blogIT.apps.profiles.models import Profile

from .models import User


@receiver(post_save, sender=User)
def create_related_profile(sender, instance, created, *args, **kwargs):
    # checking for `created` here. Only want to do this
    # the first time the `User` instance is created.
    if instance and created:
        instance.profile = Profile.objects.create(user=instance)
