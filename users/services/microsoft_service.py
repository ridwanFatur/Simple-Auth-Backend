import requests
from django.core.exceptions import ValidationError


class MicrosoftService:
    def get_account_by_auth_code(auth_code: str):
        headers = {
            "Authorization": f"Bearer {auth_code}",
            "Content-Type": "application/json",
        }
        response = requests.get("https://graph.microsoft.com/v1.0/me", headers=headers)

        if not response.ok:
            raise ValidationError("Invalid credential.")

        return response.json()
