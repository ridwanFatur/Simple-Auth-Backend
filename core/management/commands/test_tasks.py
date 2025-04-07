from django.core.management import BaseCommand
from django.template.loader import render_to_string

from core.services.email_service import EmailService
from user_settings.services.verification_service import VerificationService
from users.models import UserModel


class Command(BaseCommand):
    def execute(self, *args, **options):
        test_send_email_verification()
        # test_send_email()
        pass


def test_send_email_verification():
    user = UserModel.objects.filter(
        email="ridwan.faturrahman.godjali@gmail.com"
    ).first()
    VerificationService.send_verification_email(user)
    pass


def test_send_email():
    html_content = render_to_string(
        "dummy_email_template.html", {"name": "John Doe", "message": "Special Message"}
    )

    success = EmailService.send_email(
        subject="Email Subject",
        recipient_list=["ridwan.faturrahman.godjali@gmail.com"],
        html_content=html_content,
        cc=["cc@example.com"],
    )

    if success:
        print("Success")
    else:
        print("Failed")
