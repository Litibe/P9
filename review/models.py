from django.core.validators import MinValueValidator, MaxValueValidator
from django.conf import settings
from django.db import models
from authentication.models import User
from django.utils import timezone


class Ticket(models.Model):
    title = models.CharField(max_length=128, null=True,
                             blank=True, verbose_name="Titre du Ticket")
    description = models.TextField(max_length=2048, blank=True, null=True)
    user = models.ForeignKey(
        to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank=True, null=True)
    image = models.ImageField(null=True, blank=True)
    time_created = models.DateTimeField(
        default=timezone.now)


class Review(models.Model):
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE)
    rating = models.PositiveSmallIntegerField(
        # validates that rating must be between 0 and 5
        validators=[MinValueValidator(0), MaxValueValidator(5)], verbose_name="Note", help_text="Note attribuée à la critique")
    headline = models.CharField(
        max_length=128, blank=True, null=True,  verbose_name="Titre de Critique")
    body = models.TextField(max_length=8192, blank=True,
                            null=True,  verbose_name="Commentaire")
    user = models.ForeignKey(
        to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank=True, null=True)
    time_created = models.DateTimeField(
        default=timezone.now)


class UserFollows(models.Model):
    user = models.ForeignKey(
        to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="following", null=True,)
    followed_user = models.ForeignKey(
        to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="followed_by", null=True,)

    class Meta:
        # ensures we don't get multiple UserFollows instances
        # for unique user-user_followed pairs
        unique_together = ('user', 'followed_user')
