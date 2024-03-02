from django.db import models
from django.contrib.auth.models import AbstractUser
from shortuuid import ShortUUID
from shortuuid.django_fields import ShortUUIDField


class User(AbstractUser):
    userId = ShortUUIDField(
        length=16,
        max_length=16,
        # prefix="id_",
        alphabet="abcdefg1234",
        # primary_key=True,
    )
    image = models.ImageField(
        upload_to="users", blank=True, null=True)


class OnlineUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username
