from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from PIL import Image


class User(AbstractUser):
    profile_photo = models.ImageField(
        upload_to=settings.MEDIA_ROOT.joinpath('profile/'), verbose_name='Photo de profil')

    IMAGE_MAX_SIZE = (300, 300)

    def resize_image(self):
        profile_photo = Image.open(self.profile_photo)
        profile_photo.thumbnail(self.IMAGE_MAX_SIZE)
        profile_photo.save(self.profile_photo.path)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.resize_image()
