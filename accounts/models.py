from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)
from django.db import models



class UserManager(BaseUserManager):
    use_in_migrations = True

    def create_user(self, email, name, password=None, **kwargs):
        """Creates and saves a User"""
        if not email:
            raise ValueError('User must have an email address')

        user = self.model(
            email=self.normalize_email(email),
            name=name,
            **kwargs,
        )
        if user.is_admin and not password:
            raise ValueError("Can't create an admin without a password")

        if password:
            user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, name, password=None, **kwargs):
        """Creates and saves a superuser"""
        user = self.create_user(
            email, name, password=password, **kwargs
        )
        user.is_admin = True

        user.save(using=self._db)
        return user


class Location(models.Model):
    # SASB, etc.
    common_name = models.CharField(max_length=200)

    def __str__(self):
        return self.common_name

        class Meta:
            ordering = ('common_name', )


class User(AbstractBaseUser, PermissionsMixin):
    name = models.CharField(max_length=255)
    nickname = models.CharField(max_length=255, null=True)
    email = models.CharField(max_length=255, unique=True)
    description = models.TextField()
    location_only = models.BooleanField(default=False)

    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)

    # acceptable locations for this user to meet at
    locations = models.ManyToManyField(Location)

    USERNAME_FIELD = 'email'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = ['name']

    objects = UserManager()

    def __str__(self):
        #TODO: concatenate name and locations
        return ('Name: {name}\n'
        'Locations: {locations}\n'
        ).format(**self.__dict__)

    def get_full_name(self):
        return self.name

    def get_short_name(self):
        if self.nickname:
            return self.nickname
        return self.name


