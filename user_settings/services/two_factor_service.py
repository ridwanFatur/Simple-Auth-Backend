import pyotp
from django.conf import settings
from django.core.exceptions import ValidationError

from user_settings.constants import METHOD_AUTHENTICATOR
from user_settings.models.two_factor_setting import (
    TemporaryLoginToken,
    TwoFactorSettingModel,
)
from users.models import UserModel


class TwoFactorSettingService:
    @staticmethod
    def enable_two_factor_setting(user: UserModel):
        two_factor_settings = TwoFactorSettingModel.objects.filter(
            user=user, is_active=True
        )
        if len(two_factor_settings) == 0:
            raise ValidationError("There is no selected 2FA method available")

        user.enable_2fa = True
        user.save(update_fields=["enable_2fa"])

    @staticmethod
    def disable_two_factor_setting(user: UserModel, method: str, otp_code: str):
        if method == METHOD_AUTHENTICATOR:
            TwoFactorMethodService.verify_authenticator_app_method(user, otp_code)
        else:
            raise ValidationError("It is not implemented yet")

        user.enable_2fa = False
        user.save(update_fields=["enable_2fa"])

    @staticmethod
    def verify_login(
        otp_code: str, type: str, login_token: str, method: str
    ) -> TemporaryLoginToken:
        login_token_model = TemporaryLoginToken.objects.filter(
            type=type,
            token=login_token,
            is_used=False,
        ).first()
        if not login_token_model:
            raise ValidationError("Something went wrong")
        user = login_token_model.user

        if method == METHOD_AUTHENTICATOR:
            TwoFactorMethodService.verify_authenticator_app_method(user, otp_code)
        else:
            raise ValidationError("It is not implemented yet")

        login_token_model.is_used = True
        login_token_model.save(update_fields=["is_used"])
        return login_token_model

    @staticmethod
    def create_login_token(user: UserModel, type: str) -> TemporaryLoginToken:
        login_token = TemporaryLoginToken.objects.create(
            user=user,
            type=type,
        )
        return login_token


class TwoFactorMethodService:
    @staticmethod
    def get_available_methods(user: UserModel):
        two_factor_settings = TwoFactorSettingModel.objects.filter(
            user=user, is_active=True
        )
        return two_factor_settings

    @staticmethod
    def add_two_factor_method(user: UserModel, method: str):
        if method == METHOD_AUTHENTICATOR:
            return TwoFactorMethodService.set_authenticator_app_method(user)
        else:
            raise ValidationError("It is not implemented yet")

    @staticmethod
    def enable_two_factor_method(user: UserModel, method: str, otp_code: str):
        if method == METHOD_AUTHENTICATOR:
            two_factor_setting = TwoFactorMethodService.verify_authenticator_app_method(
                user, otp_code
            )
        else:
            raise ValidationError("It is not implemented yet")

        two_factor_setting.is_active = True
        two_factor_setting.save(update_fields=["is_active"])

    @staticmethod
    def disable_two_factor_method(user: UserModel, method: str, otp_code: str):
        if user.enable_2fa:
            raise ValidationError("Disable 2FA Mode First")

        if method == METHOD_AUTHENTICATOR:
            two_factor_setting = TwoFactorMethodService.verify_authenticator_app_method(
                user, otp_code
            )
        else:
            raise ValidationError("It is not implemented yet")

        two_factor_setting.is_active = False
        two_factor_setting.save(update_fields=["is_active"])

    @staticmethod
    def set_authenticator_app_method(user: UserModel):
        secret_key = pyotp.random_base32()
        two_factor_setting, created = TwoFactorSettingModel.objects.update_or_create(
            user=user, method=METHOD_AUTHENTICATOR, defaults={"secret_key": secret_key}
        )
        if not created:
            two_factor_setting.secret_key = secret_key
            two_factor_setting.save(update_fields=["secret_key"])
        totp = pyotp.TOTP(secret_key)
        qr_url = totp.provisioning_uri(name=user.email, issuer_name=settings.APP_NAME)
        return {"qr_url": qr_url, "secret": secret_key}

    @staticmethod
    def verify_authenticator_app_method(user: UserModel, otp_code: str):
        two_factor_setting = TwoFactorSettingModel.objects.filter(
            user=user, method=METHOD_AUTHENTICATOR
        ).first()
        if not two_factor_setting:
            raise ValidationError(
                "Authenticator App Method - 2FA is not enabled for this account."
            )
        if not pyotp.TOTP(two_factor_setting.secret_key).verify(otp_code):
            raise ValidationError("Invalid code")

        return two_factor_setting
