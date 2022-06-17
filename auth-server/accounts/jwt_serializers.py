from accounts.models import SocialUser

from django.conf import settings
from django.contrib.auth.models import update_last_login

from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from rest_framework_simplejwt.settings import api_settings
from rest_framework_simplejwt.tokens import RefreshToken, UntypedToken
from rest_framework_simplejwt.serializers import TokenObtainSerializer

if api_settings.BLACKLIST_AFTER_ROTATION:
    from rest_framework_simplejwt.token_blacklist.models import BlacklistedToken


class TokenVerifySerializer(serializers.Serializer):
    access_token = serializers.CharField()
    expires_in = serializers.IntegerField(read_only=True)

    def validate(self, attrs):
        token = UntypedToken(attrs["access_token"])

        if (
            api_settings.BLACKLIST_AFTER_ROTATION
            and "rest_framework_simplejwt.token_blacklist" in settings.INSTALLED_APPS
        ):
            jti = token.get(api_settings.JTI_CLAIM)
            if BlacklistedToken.objects.filter(token__jti=jti).exists():
                raise ValidationError("Token is blacklisted")

        return {}


class TokenRefreshSerializer(serializers.Serializer):
    access_token = serializers.CharField(read_only=True)
    expires_in = serializers.IntegerField(read_only=True)
    refresh_token = serializers.CharField()
    refresh_token_expires_in = serializers.IntegerField(read_only=True)

    token_class = RefreshToken

    def validate(self, attrs):
        refresh = self.token_class(attrs["refresh_token"])

        data = {
            "access_token": str(refresh.access_token),
            "expires_in": refresh.access_token.lifetime.total_seconds()
        }

        if api_settings.ROTATE_REFRESH_TOKENS:
            if api_settings.BLACKLIST_AFTER_ROTATION:
                try:
                    # Attempt to blacklist the given refresh token
                    refresh.blacklist()
                except AttributeError:
                    # If blacklist app not installed, `blacklist` method will
                    # not be present
                    pass

            refresh.set_jti()
            refresh.set_exp()
            refresh.set_iat()

        data.update({
            "refresh_token": str(refresh),
            "refresh_token_expires_in": refresh.lifetime.total_seconds()
        })

        return data


class TokenUserSerializer(serializers.ModelSerializer):
    """
    로그인 성공 시 반환하는 사용자 정보
    """

    class Meta:
        model = SocialUser
        fields = ['id']
        extra_kwargs = {
            'id': {'help_text': 'User ID'},
        }


class TokenObtainPairSerializer(TokenObtainSerializer):
    access_token = serializers.CharField(read_only=True, help_text='Baton App 인증을 위한 Access Token')
    expires_in = serializers.IntegerField(read_only=True)
    refresh_token = serializers.CharField(read_only=True, help_text='Baton App Access Token 갱신을 위한 Refresh Token')
    refresh_token_expires_in = serializers.IntegerField(read_only=True)
    user = TokenUserSerializer(read_only=True)

    token_class = RefreshToken

    def validate(self, attrs):
        data = super().validate(attrs)
        data.update(self.get_token(self.user))

        if api_settings.UPDATE_LAST_LOGIN:
            update_last_login(None, self.user)

        return data

    @classmethod
    def get_token(cls, user):
        refresh = cls.token_class.for_user(user)

        token = {
            "access_token": str(refresh.access_token),
            "expires_in": refresh.access_token.lifetime.total_seconds(),
            "refresh_token": str(refresh),
            "refresh_token_expires_in": refresh.lifetime.total_seconds(),
            "user": TokenUserSerializer(user).data
        }
        return token
