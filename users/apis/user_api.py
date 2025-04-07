from rest_framework.request import Request
from rest_framework.response import Response

from core.base.base_api import BaseAPI
from users.serializers.user_serializer import UserSerializer


class UserAPI(BaseAPI):
    # Default API Methods
    def list(self, request: Request):
        return Response(UserSerializer(instance=request.user).data)
