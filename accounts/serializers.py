import requests

from rest_framework import serializers


class SocialLoginSerializer(serializers.Serializer):
    access_token = serializers.CharField(required=True)
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

