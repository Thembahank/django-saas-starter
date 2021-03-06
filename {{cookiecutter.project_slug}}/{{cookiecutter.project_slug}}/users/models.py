# Django
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from django.utils.translation import gettext_lazy as _


class UserQuerySet(models.QuerySet):
    def matches_usernames(self, names):
        """Returns users matching the (case insensitive) username.

        Args:
            names (list): list of usernames

        Returns:
            QuerySet
        """
        if not names:
            return self.none()
        return self.filter(username__iregex=r"^(%s)+" % "|".join(names))


class UserManager(BaseUserManager.from_queryset(UserQuerySet)):
    def create_user(self, username, email, password=None, **kwargs):
        user = self.model(
            username=username, email=self.normalize_email(email), **kwargs
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password, **kwargs):
        return self.create_user(
            username,
            email,
            password,
            is_staff=True,
            is_superuser=True,
            **kwargs,
        )


class User(AbstractUser):
    name = models.CharField(_("Full name"), blank=True, max_length=255)

    objects = UserManager()
