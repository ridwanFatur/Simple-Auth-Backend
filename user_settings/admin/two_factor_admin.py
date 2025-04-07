from django.contrib import admin


class TwoFactorSettingAdmin(admin.ModelAdmin):
    list_display = ("user", "method")


class TemporaryLoginTokenAdmin(admin.ModelAdmin):
    list_display = ("user", "token", "is_used", "type")
