from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from rest_framework.request import Request
from rest_framework.response import Response

from core.base.base_api import BaseAPI
from user_settings.serializers.two_factor_serializer import (
    AddTwoFactorSettingSerializer,
    DisaleTwoFactorModeSerializer,
    LoginTwoFactorSerializer,
    TwoFactorSettingSerializer,
    VerifyTwoFactorSettingSerializer,
)
from user_settings.services.two_factor_service import (
    TwoFactorMethodService,
    TwoFactorSettingService,
)
from users.serializers.user_serializer import UserWithTokenSerializer
from users.services.authentication_service import AuthenticationService


class TwoFactorSettingAPI(BaseAPI):
    # Enable 2FA
    @action(
        detail=False,
        methods=["POST"],
        url_path="enable",
    )
    def enable_2fa(self, request: Request):
        TwoFactorSettingService.enable_two_factor_setting(request.user)
        return Response({})

    # Disable 2FA
    @action(
        detail=False,
        methods=["POST"],
        url_path="disable",
    )
    def disable_2fa(self, request: Request):
        data = DisaleTwoFactorModeSerializer(data=request.data)
        data.is_valid(raise_exception=True)

        TwoFactorSettingService.disable_two_factor_setting(
            user=request.user,
            method=data.validated_data["method"],
            otp_code=data.validated_data["otp_code"],
        )
        return Response({})

    # Verify 2FA to Login
    @action(
        detail=False,
        methods=["POST"],
        url_path="login",
        permission_classes=[AllowAny],
    )
    def verify_login(self, request: Request):
        data = LoginTwoFactorSerializer(data=request.data)
        data.is_valid(raise_exception=True)
        login_token_model = TwoFactorSettingService.verify_login(
            method=data.validated_data["method"],
            otp_code=data.validated_data["otp_code"],
            type=data.validated_data["type"],
            login_token=data.validated_data["login_token"],
        )

        serializer_payload = AuthenticationService.get_user_with_token_payload(
            login_token_model.user
        )
        return Response(UserWithTokenSerializer(serializer_payload).data)


class TwoFactorMethodAPI(BaseAPI):
    def list(self, request: Request):
        serializer = TwoFactorSettingSerializer(
            instance=TwoFactorMethodService.get_available_methods(request.user),
            many=True,
        )
        return Response(serializer.data)

    # Add 2FA Method
    @action(
        detail=False,
        methods=["POST"],
        url_path="add",
    )
    def add_method(self, request: Request):
        data = AddTwoFactorSettingSerializer(data=request.data)
        data.is_valid(raise_exception=True)

        result = TwoFactorMethodService.add_two_factor_method(
            user=request.user, method=data.validated_data["method"]
        )

        return Response(result)

    # Enable 2FA Method
    @action(
        detail=False,
        methods=["POST"],
        url_path="enable",
    )
    def enable_method(self, request: Request):
        data = VerifyTwoFactorSettingSerializer(data=request.data)
        data.is_valid(raise_exception=True)

        TwoFactorMethodService.enable_two_factor_method(
            user=request.user,
            method=data.validated_data["method"],
            otp_code=data.validated_data["otp_code"],
        )

        return Response({})

    # Disale 2FA Method
    @action(
        detail=False,
        methods=["POST"],
        url_path="disable",
    )
    def disable_method(self, request: Request):
        data = VerifyTwoFactorSettingSerializer(data=request.data)
        data.is_valid(raise_exception=True)

        TwoFactorMethodService.disable_two_factor_method(
            user=request.user,
            method=data.validated_data["method"],
            otp_code=data.validated_data["otp_code"],
        )

        return Response({})
