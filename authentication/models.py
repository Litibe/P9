from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings


class User(AbstractUser):
    profile_photo = models.ImageField(
        upload_to=settings.MEDIA_ROOT.joinpath('profile/'), verbose_name='Photo de profil')
