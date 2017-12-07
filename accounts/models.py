from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)
from django.db import models


class UserManager(BaseUserManager):
    use_in_migrations = True

    def create_user(self, email, name, credential, description=None):
        """Creates and saves a User"""
        if not email:
            raise ValueError('User must have an email address')

        user = self.model(
            email=self.normalize_email(email),
            name=name,
            description=description,
        )

        user.save(using=self._db)
        return user

    def create_superuser(self, email, name, credential, description=None):
        """Creates and saves a superuser"""
        user = self.create_user(
            email, name, credential,
            description=description,
        )
        user.is_admin = True

        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    name = models.CharField(max_length=255)
    nickname = models.CharField(max_length=255)
    email = models.CharField(max_length=255, unique=True)
    description = models.TextField()

    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = ['name']

    objects = UserManager()

    def get_full_name(self):
        return self.name

    def get_short_name(self):
        if self.nickname:
            return self.nickname
        return self.name
