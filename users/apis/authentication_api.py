from django.db import transaction
from django.utils.timezone import now
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from core.base.base_api import BaseAPI
from user_settings.services.two_factor_service import TwoFactorSettingService
from user_settings.services.verification_service import VerificationService
from users.models import UserModel
from users.serializers.authentication_serializer import (
    GoogleSigninSerializer,
    GoogleSignupSerializer,
    MicrosoftSigninSerializer,
    MicrosoftSignupSerializer,
    PasswordSigninSerializer,
    PasswordSignupSerializer,
)
from users.serializers.user_serializer import UserWithTokenSerializer
from users.services.authentication_service import AuthenticationService


class AuthenticationAPIUtils:
    @staticmethod
    def handle_sign_in(user: UserModel, type: str):
        user.last_login = now()
        user.save(update_fields=["last_login"])

        if user.enable_2fa:
            login_token = TwoFactorSettingService.create_login_token(
                user=user, type=type
            )
            return Response({"requires_otp": True, "login_token": login_token.token})

        serializer_payload = AuthenticationService.get_user_with_token_payload(user)
        return Response(
            UserWithTokenSerializer(serializer_payload).data,
        )

    @staticmethod
    def handle_sign_up(user: UserModel):
        user.last_login = now()
        user.save(update_fields=["last_login"])

        # VerificationService.send_verification_email(user)

        serializer_payload = AuthenticationService.get_user_with_token_payload(user)
        return Response(
            UserWithTokenSerializer(serializer_payload).data,
            status=status.HTTP_201_CREATED,
        )


class PasswordEmailAuthAPI(BaseAPI):
    # Password - Sign In
    @action(
        detail=False,
        methods=["POST"],
        url_path="signin",
        permission_classes=[AllowAny],
    )
    def password_signin(self, request):
        data = PasswordSigninSerializer(data=request.data)
        data.is_valid(raise_exception=True)

        user = AuthenticationService.PasswordEmailMethod.signin(
            email=data.validated_data["email"], password=data.validated_data["password"]
        )
        response = AuthenticationAPIUtils.handle_sign_in(user=user, type="email")
        return response

    # Password - Sign Up
    @action(
        detail=False,
        methods=["POST"],
        url_path="signup",
        permission_classes=[AllowAny],
    )
    @transaction.atomic
    def password_signup(self, request):
        data = PasswordSignupSerializer(data=request.data)
        data.is_valid(raise_exception=True)

        new_user = AuthenticationService.PasswordEmailMethod.signup(
            email=data.validated_data["email"],
            password=data.validated_data["password"],
            full_name=data.validated_data["full_name"],
            role=data.validated_data["role"],
        )
        response = AuthenticationAPIUtils.handle_sign_up(user=new_user)
        return response


class GoogleAuthAPI(BaseAPI):
    # Google - Sign In
    @action(
        detail=False,
        methods=["POST"],
        url_path="signin",
        permission_classes=[AllowAny],
    )
    def google_signin(self, request):
        data = GoogleSigninSerializer(data=request.data)
        data.is_valid(raise_exception=True)

        user = AuthenticationService.GoogleMethod.signin(
            auth_code=data.validated_data["auth_code"],
        )
        response = AuthenticationAPIUtils.handle_sign_in(user=user, type="google")
        return response

    # Google - Sign Up
    @action(
        detail=False,
        methods=["POST"],
        url_path="signup",
        permission_classes=[AllowAny],
    )
    @transaction.atomic
    def google_signup(self, request):
        data = GoogleSignupSerializer(data=request.data)
        data.is_valid(raise_exception=True)

        new_user = AuthenticationService.GoogleMethod.signup(
            auth_code=data.validated_data["auth_code"],
            role=data.validated_data["role"],
        )
        response = AuthenticationAPIUtils.handle_sign_up(user=new_user)
        return response


class MicrosoftAuthAPI(BaseAPI):
    # Microsoft - Sign In
    @action(
        detail=False,
        methods=["POST"],
        url_path="signin",
        permission_classes=[AllowAny],
    )
    def microsoft_signin(self, request):
        data = MicrosoftSigninSerializer(data=request.data)
        data.is_valid(raise_exception=True)

        user = AuthenticationService.MicrosoftMethod.signin(
            auth_code=data.validated_data["auth_code"],
        )
        response = AuthenticationAPIUtils.handle_sign_in(user=user, type="microsoft")
        return response

    # Microsoft - Sign Up
    @action(
        detail=False,
        methods=["POST"],
        url_path="signup",
        permission_classes=[AllowAny],
    )
    @transaction.atomic
    def microsoft_signup(self, request):
        data = MicrosoftSignupSerializer(data=request.data)
        data.is_valid(raise_exception=True)

        new_user = AuthenticationService.MicrosoftMethod.signup(
            auth_code=data.validated_data["auth_code"],
            role=data.validated_data["role"],
        )
        response = AuthenticationAPIUtils.handle_sign_up(user=new_user)
        return response
