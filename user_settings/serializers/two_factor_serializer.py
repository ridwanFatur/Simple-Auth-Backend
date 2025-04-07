from rest_framework import serializers

from user_settings.constants import METHOD_CHOICES
from user_settings.models.two_factor_setting import TwoFactorSettingModel


# 2FA User Setting
class DisaleTwoFactorModeSerializer(serializers.Serializer):
    otp_code = serializers.CharField(required=True)
    method = serializers.ChoiceField(required=True, choices=METHOD_CHOICES)


class LoginTwoFactorSerializer(serializers.Serializer):
    otp_code = serializers.CharField(required=True)
    method = serializers.ChoiceField(required=True, choices=METHOD_CHOICES)
    type = serializers.CharField(required=True)
    login_token = serializers.CharField(required=True)


# 2FA Methods
class TwoFactorSettingSerializer(serializers.ModelSerializer):
    class Meta:
        model = TwoFactorSettingModel
        fields = ["uid", "method"]


class AddTwoFactorSettingSerializer(serializers.Serializer):
    method = serializers.ChoiceField(required=True, choices=METHOD_CHOICES)


class VerifyTwoFactorSettingSerializer(serializers.Serializer):
    otp_code = serializers.CharField(required=True)
    method = serializers.ChoiceField(required=True, choices=METHOD_CHOICES)
