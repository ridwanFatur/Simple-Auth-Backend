from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from core.base.base_api import BaseAPI
from user_settings.serializers.verification_serializer import VerifyEmailSerializer
from user_settings.services.verification_service import VerificationService


class VerificationAPI(BaseAPI):
    @action(
        detail=False,
        methods=["POST"],
        url_path="verify",
        permission_classes=[AllowAny],
    )
    def verify(self, request):
        data = VerifyEmailSerializer(data=request.data)
        data.is_valid(raise_exception=True)

        VerificationService.verify_code(
            code=data.validated_data["code"], email=data.validated_data["email"]
        )
        return Response({})

    @action(
        detail=False,
        methods=["POST"],
        url_path="send_email",
    )
    def send_email(self, request):
        VerificationService.send_verification_email(request.user)
        return Response({})
