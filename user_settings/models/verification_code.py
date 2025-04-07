from datetime import timedelta

from django.db import models
from django.utils import timezone

from users.base.base_user_related_model import UserRequiredBaseModel
from users.models import UserModel


class VerificationCodeModel(UserRequiredBaseModel):
    user = models.ForeignKey(
        UserModel, on_delete=models.CASCADE, related_name="verification_codes"
    )
    code = models.CharField(max_length=8, unique=True)
    expires_at = models.DateTimeField()
    verified_at = models.DateTimeField(null=True, blank=True)
    is_verified = models.BooleanField(default=False)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"Verification code for {self.user.email}"

    def save(self, *args, **kwargs):
        # Generate a random code if not provided
        if not self.code:
            self.code = self.generate_verification_code()

        # Set expiration time if not provided
        if not self.expires_at:
            # Default expiration: 24 hours from creation
            self.expires_at = timezone.now() + timedelta(hours=24)

        super().save(*args, **kwargs)

    @staticmethod
    def generate_verification_code():
        """Generate a random 6-character alphanumeric code"""
        import random
        import string

        chars = string.ascii_uppercase + string.digits
        return "".join(random.choice(chars) for _ in range(6))

    def is_expired(self):
        """Check if the verification code has expired"""
        return timezone.now() > self.expires_at

    def verify(self):
        """Mark the code as verified"""
        self.is_verified = True
        self.verified_at = timezone.now()
        self.save()
        return True
