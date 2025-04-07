import uuid

import pyotp
from django.db import models

from user_settings.constants import METHOD_CHOICES
from users.base.base_user_related_model import UserRequiredBaseModel


class TwoFactorSettingModel(UserRequiredBaseModel):
    secret_key = models.CharField(max_length=255, blank=True, null=True)
    method = models.CharField(max_length=50, choices=METHOD_CHOICES)
    backup_codes = models.JSONField(default=list, blank=True)
    is_active = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.email} - {self.method}"

    def get_totp(self):
        """Return a TOTP object based on the secret key"""
        if not self.secret_key:
            return None
        return pyotp.TOTP(self.secret_key)

    def verify_code(self, code):
        """Verify the provided code against the TOTP"""
        totp = self.get_totp()
        if not totp:
            return False

        # Check if it's a backup code
        if code in self.backup_codes:
            # Remove the used backup code
            self.backup_codes.remove(code)
            self.save()
            return True

        # Otherwise check against TOTP
        return totp.verify(code)


class TemporaryLoginToken(UserRequiredBaseModel):
    token = models.UUIDField(default=uuid.uuid4, editable=False)
    is_used = models.BooleanField(default=False)
    type = models.CharField(max_length=200)
