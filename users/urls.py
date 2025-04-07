from django.urls import include, path
from rest_framework import routers

from users.apis.authentication_api import (
    GoogleAuthAPI,
    MicrosoftAuthAPI,
    PasswordEmailAuthAPI,
)
from users.apis.jwt_token_api import JWTTokenAPI
from users.apis.user_api import UserAPI

api_router = routers.DefaultRouter()
api_router.register(r"", UserAPI, basename="")
api_router.register(r"auth", PasswordEmailAuthAPI, basename="auth")
api_router.register(r"google_auth", GoogleAuthAPI, basename="google_auth")
api_router.register(r"microsoft_auth", MicrosoftAuthAPI, basename="microsoft_auth")
api_router.register(r"token", JWTTokenAPI, basename="token")


urlpatterns = [path("", include(api_router.urls))]
