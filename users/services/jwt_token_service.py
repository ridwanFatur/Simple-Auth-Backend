from rest_framework_simplejwt.tokens import AccessToken, RefreshToken

from users.models import UserModel


class JWTTokenService:
    @staticmethod
    def generate_jwt_token(user: UserModel) -> tuple[str, str]:
        refresh = RefreshToken.for_user(user)
        access = AccessToken.for_user(user)
        return str(refresh), str(access)

    @staticmethod
    def generate_access_token_from_refresh_token(refresh_token: str) -> str:
        refresh = RefreshToken(refresh_token)
        access_token = str(refresh.access_token)
        return access_token
