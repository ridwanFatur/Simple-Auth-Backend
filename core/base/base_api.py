import logging

from django.core.exceptions import ValidationError
from django.http import JsonResponse
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework.exceptions import APIException
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication

from core.base.base_pagination import BasePagination

log = logging.getLogger(__name__)


class BaseAPI(viewsets.GenericViewSet):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    pagination_class = BasePagination
    filter_backends = [DjangoFilterBackend]

    def initial(self, request, *args, **kwargs):
        super().initial(request, *args, **kwargs)

    def handle_exception(self, exc):
        """
        Handle exceptions that occur during API requests.
        """
        if isinstance(exc, APIException):
            log.error(f"API error: {exc.detail}")
            return JsonResponse(
                {"errors": [exc.detail], "code": exc.default_code},
                status=exc.status_code,
            )

        if isinstance(exc, ValidationError):
            log.warning(f"Validation error: {exc}")
            return JsonResponse({"errors": exc.messages}, status=400)

        if isinstance(exc, Exception):
            log.error(f"Unhandled exception: {exc}")
            return JsonResponse({"errors": [str(exc)]}, status=500)

        # This is a bit redundant as we already catch all exceptions above,
        # but keeping it for robustness
        log.critical(f"Unhandled exception: {exc}", exc_info=True)
        return JsonResponse({"errors": ["Internal server error"]}, status=500)
