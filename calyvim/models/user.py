import pytz
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, AbstractUser
from django.contrib.auth.validators import UnicodeUsernameValidator

from calyvim.models.base import BaseUUIDTimestampModel


class UserManager(BaseUserManager):
    def create_user(self, username, email, full_name, password=None):
        user = self.model(
            username=username, email=self.normalize_email(email), full_name=full_name
        )
        if password:
            user.set_password(password)

        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, full_name, password):
        user = self.create_user(username, email, full_name, password)
        user.is_staff = True
        user.verified_at = timezone.now()
        user.save(using=self._db)
        return user


class User(BaseUUIDTimestampModel, AbstractBaseUser):
    username_validator = UnicodeUsernameValidator()
    TIMEZONE_CHOICES = tuple(zip(pytz.all_timezones, pytz.all_timezones))

    username = models.CharField(
        max_length=150,
        unique=True,
        validators=[username_validator],
        help_text="Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.",
        error_messages={"unique": "A user with that username already exists."},
    )
    email = models.EmailField(
        unique=True, error_messages={"unique": "A user with that email already exists"}
    )
    full_name = models.CharField(verbose_name="full name", max_length=150)
    phone = models.CharField(max_length=30, blank=True, null=True)
    avatar = models.ImageField(upload_to="users/avatars/", blank=True, null=True)

    is_active = models.BooleanField(
        verbose_name="active status",
        default=True,
        help_text="Designates whether the user can log into site.",
    )
    is_staff = models.BooleanField(
        verbose_name="staff status",
        default=False,
        help_text="Designates whether the user can log into this admin site.",
    )
    is_password_expired = models.BooleanField(
        verbose_name="password expiration status",
        default=False,
        help_text="Designates whether the user needs to reset the password in order to login to the site.",
    )
    timezone = models.CharField(max_length=50, choices=TIMEZONE_CHOICES, default="UTC")

    verified_at = models.DateTimeField(
        verbose_name="verified on", blank=True, null=True
    )

    objects = UserManager()

    EMAIL_FIELD = "email"
    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ["email", "full_name"]

    class Meta:
        db_table = "users"

    def __str__(self) -> str:
        return self.username

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True