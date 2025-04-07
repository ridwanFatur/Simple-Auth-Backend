from django.conf import settings
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path(f"{settings.ADMIN_URL}/", admin.site.urls),
    path("api/v1/user/", include("users.urls"), name="api-user"),
    path("api/v1/settings/", include("user_settings.urls"), name="api-settings"),
]
