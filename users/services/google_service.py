import requests
from django.conf import settings
from django.core.exceptions import ValidationError


class GoogleService:
    def get_account_by_auth_code(auth_code: str, auth_type: str = "login"):
        # Get access token from auth code
        response = requests.post(
            "https://oauth2.googleapis.com/token",
            headers={"Content-Type": "application/x-www-form-urlencoded"},
            data={
                "code": auth_code,
                "client_id": settings.GOOGLE_CLIENT_ID,
                "client_secret": settings.GOOGLE_CLIENT_SECRET,
                "redirect_uri": f"{settings.FRONTEND_URL}/auth/{auth_type}",
                "grant_type": "authorization_code",
            },
        )
        if not response.ok:
            raise ValidationError("Invalid credential.")

        access_token = response.json()["access_token"]

        # Get user info
        response = requests.get(
            f"https://www.googleapis.com/oauth2/v1/userinfo?access_token={access_token}",
            headers={
                "Authorization": f"Bearer {access_token}",
                "Accept": "application/json",
            },
        )

        if not response.ok:
            raise ValidationError("Invalid credential.")

        return response.json()
