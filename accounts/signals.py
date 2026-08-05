from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import CustomUser


@receiver(post_save, sender=CustomUser)
def create_user_profile(sender, instance, created, **kwargs):
    """
    Runs after a new user is created.
    You can add default setup here.
    """
    if created:
        print(f"New user created: {instance.username}")


@receiver(post_save, sender=CustomUser)
def save_user_profile(sender, instance, **kwargs):
    """
    Runs whenever a user is saved.
    """
    pass  