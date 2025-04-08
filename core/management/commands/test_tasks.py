import os
import re

from django.core.management import BaseCommand
from django.template.loader import render_to_string

from core.services.email_service import EmailService
from user_settings.services.verification_service import VerificationService
from users.models import UserModel


class Command(BaseCommand):
    def execute(self, *args, **options):
        print("Only This")
        # get_all_requirements()
        # test_send_email_verification()
        # test_send_email()
        pass


def get_all_requirements():
    imports = set()

    for root, dirs, files in os.walk("."):
        for file in files:
            if file.endswith(".py"):
                file_path = os.path.join(root, file)
                with open(file_path, "r", encoding="utf-8") as f:
                    for line in f:
                        line = line.strip()
                        if re.match(r"^(from|import) ", line):
                            imports.add(line)

    for imp in sorted(imports):
        print(imp)


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
