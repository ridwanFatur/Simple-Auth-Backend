from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)
from django.db import models

from core.base.base_model import BaseModel
from users.constants import ROLE_SUPER_ADMIN, ROLE_USER, USER_ROLES


class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("The Email field must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        if password:
            user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("role", ROLE_SUPER_ADMIN)
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        return self.create_user(email, password, **extra_fields)


class UserModel(AbstractBaseUser, PermissionsMixin, BaseModel):
    # Basic fields
    email = models.EmailField(unique=True)
    full_name = models.CharField(max_length=255)
    role = models.CharField(max_length=20, choices=USER_ROLES, default=ROLE_USER)
    last_login = models.DateTimeField(null=True, blank=True)

    # User Settings
    google_id = models.CharField(max_length=150, null=True, blank=True, unique=True)
    microsoft_id = models.CharField(max_length=150, null=True, blank=True, unique=True)

    # 2FA
    enable_2fa = models.BooleanField(default=False)

    # Django fields
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    # Other Configs
    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["full_name"]

    def __str__(self):
        return self.email
