from django.contrib.auth.base_user import BaseUserManager, AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.db import models
from django.utils import timezone


class UserManager(BaseUserManager):
    def create_user(self, telegram_id, password=None, username_tg=None, first_name=None, last_name=None, **extra_fields):
        if not telegram_id:
            raise ValueError('The Telegram ID must be set')

        user = self.model(
            telegram_id=telegram_id,
            username_tg=username_tg,
            first_name=first_name,
            last_name=last_name,
            **extra_fields
        )
        if password:
            user.set_password(password)
        else:
            user.set_unusable_password()
        user.save(using=self._db)
        return user

    def create_superuser(self, telegram_id, password, username_tg=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(
            telegram_id=telegram_id,
            password=password,
            username_tg=username_tg,
            **extra_fields
        )


class User(AbstractBaseUser, PermissionsMixin):
    """Custom user model for Telegram authentication"""
    telegram_id = models.BigIntegerField(unique=True, db_index=True)
    username_tg = models.CharField(max_length=32, blank=True, null=True)
    first_name = models.CharField(max_length=150, blank=True, null=True)
    last_name = models.CharField(max_length=150, blank=True, null=True)

    # EVM wallet address
    evm_address = models.CharField(max_length=42, blank=True, null=True, unique=True)

    # User permissions
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    # Timestamps
    date_joined = models.DateTimeField(default=timezone.now)
    last_login = models.DateTimeField(null=True, blank=True)

    objects = UserManager()

    USERNAME_FIELD = 'telegram_id'
    REQUIRED_FIELDS = []

    class Meta:
        db_table = 'auth_user'
        verbose_name = 'User'
        verbose_name_plural = 'Users'

    def __str__(self):
        return f"User {self.telegram_id} ({self.username_tg or 'No username'})"

    def get_full_name(self):
        if self.first_name and self.last_name:
            return f"{self.first_name} {self.last_name}"
        return self.first_name or self.username_tg or str(self.telegram_id)

    def get_short_name(self):
        return self.first_name or self.username_tg or str(self.telegram_id)
