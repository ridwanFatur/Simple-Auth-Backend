from rest_framework import serializers

from user_settings.models.verification_code import VerificationCodeModel
from users.models import UserModel


class UserSerializer(serializers.ModelSerializer):
    verified = serializers.SerializerMethodField()

    class Meta:
        model = UserModel
        fields = ["email", "full_name", "role", "verified", "enable_2fa"]

    def get_verified(self, instance: UserModel):
        verification_code = VerificationCodeModel.objects.filter(
            user=instance, is_verified=True
        ).first()
        if verification_code:
            return True
        return False


class UserWithTokenSerializer(serializers.Serializer):
    user = UserSerializer()
    access_token = serializers.CharField()
    refresh_token = serializers.CharField()
