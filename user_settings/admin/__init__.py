from django.contrib import admin

from user_settings.admin.two_factor_admin import (
    TemporaryLoginTokenAdmin,
    TwoFactorSettingAdmin,
)
from user_settings.admin.verification_code_admin import VerificationCodeAdmin
from user_settings.models.two_factor_setting import (
    TemporaryLoginToken,
    TwoFactorSettingModel,
)
from user_settings.models.verification_code import VerificationCodeModel

admin.site.register(VerificationCodeModel, VerificationCodeAdmin)
admin.site.register(TwoFactorSettingModel, TwoFactorSettingAdmin)
admin.site.register(TemporaryLoginToken, TemporaryLoginTokenAdmin)
