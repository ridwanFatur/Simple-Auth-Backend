import logging
from typing import List, Optional

from django.conf import settings
from django.core.mail import EmailMessage

logger = logging.getLogger(__name__)


class EmailService:
    @staticmethod
    def send_email(
        subject: str,
        recipient_list: List[str],
        html_content: str,
        cc: Optional[List[str]] = None,
    ) -> bool:
        from_email = settings.DEFAULT_FROM_EMAIL

        try:
            email = EmailMessage(
                subject=subject,
                body=html_content,
                from_email=from_email,
                to=recipient_list,
                cc=cc if cc else [],
            )
            email.content_subtype = "html"
            email.send(fail_silently=False)
            return True
        except Exception as e:
            logger.error(f"Failed to send email: {str(e)}")
            return False
