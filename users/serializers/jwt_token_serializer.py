from rest_framework import serializers


class RefreshTokenSerializer(serializers.Serializer):
    refresh_token = serializers.CharField(required=True)


class AccessTokenSerializer(serializers.Serializer):
    access_token = serializers.CharField()
