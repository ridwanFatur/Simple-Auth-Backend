from django.contrib.auth import authenticate
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError

from users.models import UserModel
from users.services.google_service import GoogleService
from users.services.jwt_token_service import JWTTokenService
from users.services.microsoft_service import MicrosoftService


class AuthenticationService:
    class PasswordEmailMethod:
        @staticmethod
        def signin(email: str, password: str) -> UserModel:
            user = authenticate(email=email, password=password)
            if user is None:
                raise ValidationError("Password and email doesn't match")
            return user

        @staticmethod
        def signup(email: str, password: str, full_name: str, role: str) -> UserModel:
            validate_password(password)
            is_email_registered = UserModel.objects.filter(email=email).exists()
            if is_email_registered:
                raise ValidationError("Email is already registered.")
            created_user = UserModel.objects.create_user(
                email=email, password=password, role=role, full_name=full_name
            )
            return created_user

    class GoogleMethod:
        @staticmethod
        def signin(auth_code: str) -> UserModel:
            google_account = GoogleService.get_account_by_auth_code(auth_code, "login")
            email = google_account["email"]
            user = UserModel.objects.filter(email=email).first()
            if user is None:
                raise ValidationError("There is no user with provided account")
            return user

        @staticmethod
        def signup(auth_code: str, role: str) -> UserModel:
            google_account = GoogleService.get_account_by_auth_code(
                auth_code, "register"
            )
            google_id = google_account["id"]
            email = google_account["email"]
            is_email_registered = UserModel.objects.filter(email=email).exists()
            if is_email_registered:
                raise ValidationError("Email is already registered.")
            created_user = UserModel.objects.create_user(
                email=email,
                role=role,
                full_name=email.split("@")[0],
                google_id=google_id,
            )
            return created_user

    class MicrosoftMethod:
        @staticmethod
        def signin(auth_code: str) -> UserModel:
            microsoft_account = MicrosoftService.get_account_by_auth_code(auth_code)
            email = microsoft_account["mail"]
            user = UserModel.objects.filter(email=email).first()
            if user is None:
                raise ValidationError("There is no user with provided account")
            return user

        @staticmethod
        def signup(auth_code: str, role: str) -> UserModel:
            microsoft_account = MicrosoftService.get_account_by_auth_code(auth_code)
            microsoft_id = microsoft_account["id"]
            email = microsoft_account["mail"]
            is_email_registered = UserModel.objects.filter(email=email).exists()
            if is_email_registered:
                raise ValidationError("Email is already registered.")
            created_user = UserModel.objects.create_user(
                email=email,
                role=role,
                full_name=email.split("@")[0],
                microsoft_id=microsoft_id,
            )
            return created_user

    @staticmethod
    def get_user_with_token_payload(user: UserModel):
        refresh_token, access_token = JWTTokenService.generate_jwt_token(user)
        serializer_payload = {
            "user": user,
            "access_token": access_token,
            "refresh_token": refresh_token,
        }
        return serializer_payload
