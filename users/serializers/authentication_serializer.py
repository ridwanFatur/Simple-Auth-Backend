from rest_framework import serializers

from users.constants import ALLOWED_SIGNUP_ROLES


# Password Method
class PasswordSignupSerializer(serializers.Serializer):
    password = serializers.CharField(required=True)
    email = serializers.EmailField(required=True)
    full_name = serializers.CharField(required=True)
    role = serializers.ChoiceField(required=True, choices=ALLOWED_SIGNUP_ROLES)


class PasswordSigninSerializer(serializers.Serializer):
    password = serializers.CharField(required=True)
    email = serializers.EmailField(required=True)


# Google Method
class GoogleSignupSerializer(serializers.Serializer):
    auth_code = serializers.CharField(required=True)
    role = serializers.ChoiceField(required=True, choices=ALLOWED_SIGNUP_ROLES)


class GoogleSigninSerializer(serializers.Serializer):
    auth_code = serializers.CharField(required=True)


# Microsoft Method
class MicrosoftSignupSerializer(serializers.Serializer):
    auth_code = serializers.CharField(required=True)
    role = serializers.ChoiceField(required=True, choices=ALLOWED_SIGNUP_ROLES)


class MicrosoftSigninSerializer(serializers.Serializer):
    auth_code = serializers.CharField(required=True)
