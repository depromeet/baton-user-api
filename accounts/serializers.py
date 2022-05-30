from mypage.models import User

import requests

from rest_framework import serializers


class JWTUserSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(source='social_user.id', help_text='User ID')

    class Meta:
        model = User
        fields = ['id']


class JWTSerializer(serializers.Serializer):
    access_token = serializers.CharField(help_text='Baton App 인증을 위한 Access Token')
    refresh_token = serializers.CharField(help_text='Baton App Access Token 갱신을 위한 Refresh Token')
    user = JWTUserSerializer()


class SocialLoginSerializer(serializers.Serializer):
    access_token = serializers.CharField(required=True, help_text='Kakao 서버 인증을 위한 Access Token')
    profile_url = ''

    class Meta:
        abstract = True

    def extract_uid(self, data):
        raise NotImplementedError

    def extract_common_fields(self, data):
        raise NotImplementedError

    def validate(self, attrs):
        # 카카오 인증 서버에 접속 -> 사용자 프로필 정보 알아옴
        headers = {"Authorization": f"Bearer {attrs['access_token']}"}
        response = requests.get(self.profile_url, headers=headers)
        response.raise_for_status()
        extra_data = response.json()
        attrs['id'] = self.extract_uid(extra_data)
        # attrs.update(self.extract_common_fields(extra_data))
        return attrs


class KaKaoLoginSerializer(SocialLoginSerializer):
    profile_url = "https://kapi.kakao.com/v2/user/me"

    def extract_uid(self, data):
        return str(data['id'])

    def extract_common_fields(self, data):
        email = data.get("kakao_account", {}).get("email")
        nickname = data.get("properties", {}).get("nickname")

        return dict(email=email, nickname=nickname)

