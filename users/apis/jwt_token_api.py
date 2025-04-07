from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from core.base.base_api import BaseAPI
from users.serializers.jwt_token_serializer import (
    AccessTokenSerializer,
    RefreshTokenSerializer,
)
from users.services.jwt_token_service import JWTTokenService


class JWTTokenAPI(BaseAPI):
    # Refresh Token
    @action(
        detail=False,
        methods=["POST"],
        url_path="refresh",
        permission_classes=[AllowAny],
    )
    def refresh_access_token(self, request):
        data = RefreshTokenSerializer(data=request.data)
        data.is_valid(raise_exception=True)

        refresh_token = data.validated_data["refresh_token"]
        access_token = JWTTokenService.generate_access_token_from_refresh_token(
            refresh_token
        )

        serializer_payload = {"access_token": access_token}
        return Response(AccessTokenSerializer(serializer_payload).data)
