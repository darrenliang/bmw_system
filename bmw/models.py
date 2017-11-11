from django.db import models

from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
from django.conf import settings
from django.contrib.auth.models import User


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)


class Profile(models.Model):
    name = models.CharField(max_length=128, default='')
    height = models.PositiveIntegerField(default=100)
    male = models.BooleanField(default=False)
    models.OneToOneField(User)

    def __str__(self):
        return self.name

