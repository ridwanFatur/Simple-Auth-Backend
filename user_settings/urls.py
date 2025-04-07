from django.urls import include, path
from rest_framework import routers

from user_settings.apis.two_factor_api import TwoFactorMethodAPI, TwoFactorSettingAPI
from user_settings.apis.verification_api import VerificationAPI

api_router = routers.DefaultRouter()
api_router.register(r"verification", VerificationAPI, basename="verification")
api_router.register(
    r"two_factor_setting", TwoFactorSettingAPI, basename="two_factor_setting"
)
api_router.register(
    r"two_factor_method", TwoFactorMethodAPI, basename="two_factor_method"
)

urlpatterns = [path("", include(api_router.urls))]
