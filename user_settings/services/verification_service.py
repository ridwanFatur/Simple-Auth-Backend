from django.conf import settings
from django.core.exceptions import ValidationError
from django.template.loader import render_to_string

from core.services.email_service import EmailService
from user_settings.models.verification_code import VerificationCodeModel
from users.models import UserModel


class VerificationService:
    @staticmethod
    def create_verification_code(user: UserModel):
        VerificationCodeModel.objects.filter(is_verified=False, user=user).delete()
        verification_code = VerificationCodeModel.objects.create(user=user)
        return verification_code

    @staticmethod
    def verify_code(code: str, email: str):
        user = UserModel.objects.filter(email=email).first()
        if not user:
            raise ValidationError("Account with the email doesn't exist")

        verification = VerificationCodeModel.objects.get(
            code=code, is_verified=False, user=user
        )

        if verification.is_expired():
            raise ValidationError("Expired Verification COde")
        verification.verify()

    @staticmethod
    def send_verification_email(user: UserModel):
        verification = VerificationService.create_verification_code(user)
        verification_url = (
            f"{settings.FRONTEND_URL}/verify_email/{verification.code}/{user.email}"
        )

        context = {
            "user": user,
            "verification_url": verification_url,
            "verification_code": verification.code,
            "expiration_hours": 24,
        }

        html_content = render_to_string(
            "user_settings/email_verification.html", context
        )

        subject = "Verify Your Email Address"
        recipient_list = [user.email]

        return EmailService.send_email(
            subject=subject, recipient_list=recipient_list, html_content=html_content
        )
