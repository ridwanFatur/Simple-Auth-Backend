from django.contrib import admin


class VerificationCodeAdmin(admin.ModelAdmin):
    list_display = ("code", "user", "expires_at", "is_verified")
