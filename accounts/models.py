from django.db import models

# Create your models here.
#from django.db import models
from django.contrib.auth.models import AbstractUser
from .managers import CustomUserManager


class CustomUser(AbstractUser):
    """
    Custom User Model
    """

    full_name = models.CharField(
        max_length=150
    )

    email = models.EmailField(
        unique=True
    )

    phone_number = models.CharField(
        max_length=20,
        unique=True
    )

    profile_picture = models.ImageField(
        upload_to="profile_pictures/",
        blank=True,
        null=True
    )

    address = models.TextField(
        blank=True,
        null=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    USERNAME_FIELD = "username"

    REQUIRED_FIELDS = [
        "email",
        "full_name",
        "phone_number"
    ]

    objects = CustomUserManager()

    def __str__(self):
        return self.username