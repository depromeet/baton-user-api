from accounts.models import SocialUser
from mypage.serializers import UserCreateSerializer

from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from django.conf import settings
from django.db import IntegrityError
from django.utils.translation import gettext as _

import requests


class JWTUserSerializer(serializers.ModelSerializer):
    """
    로그인 성공 시 반환하는 사용자 정보
    """

    class Meta:
        model = SocialUser
        fields = ['id']
        extra_kwargs = {
            'id': {'help_text': 'User ID'},
        }


class JWTSerializer(serializers.Serializer):
    """
    로그인 성공 시 반환하는 JWT 토큰의 내용
    """
    access_token = serializers.CharField(help_text='Baton App 인증을 위한 Access Token')
    refresh_token = serializers.CharField(help_text='Baton App Access Token 갱신을 위한 Refresh Token')
    user = JWTUserSerializer()


class SocialLoginSerializer(serializers.Serializer):
    access_token = serializers.CharField(required=True, help_text='Kakao 서버 인증을 위한 Access Token')
    required_common_fields = ['nickname']
    profile_url = ''

    class Meta:
        abstract = True

    def extract_uid(self, data):
        raise NotImplementedError

    def extract_common_fields(self, data):
        raise NotImplementedError

    def validate(self, attrs):
        # 소셜 서비스 인증 서버에 접속 -> 사용자 프로필 정보 알아옴
        headers = {"Authorization": f"Bearer {attrs['access_token']}"}
        response = requests.get(self.profile_url, headers=headers)
        response.raise_for_status()
        extra_data = response.json()
        attrs['uid'] = self.extract_uid(extra_data)
        attrs.update(self.extract_common_fields(extra_data))
        # self.validate_common_fields(attrs)
        return attrs

    def validate_common_fields(self, attrs):
        # all(field in self.required_common_fields for field in attrs)
        errors = []

        for field in self.required_common_fields:
            if not attrs.get(field, None):
                errors.append({field: [_('This field is required.')]})

        if errors:
            raise ValidationError(errors)


class KaKaoLoginSerializer(SocialLoginSerializer):
    profile_url = "https://kapi.kakao.com/v2/user/me"

    def extract_uid(self, data):
        return str(data['id'])

    def extract_common_fields(self, data):
        common_fields = {
            # 'email': data.get("kakao_account", {}).get("email"),
            'nickname': data.get("properties", {}).get("nickname"),
        }
        return common_fields


class SocialUserCreateSerializer(serializers.ModelSerializer):
    """
    회원가입 요청 시 전달 받는 데이터
    """
    user = UserCreateSerializer()

    class Meta:
        model = SocialUser
        fields = ['uid', 'provider', 'user']

    def validate_provider(self, value):
        """
        provider가 지원하는 소셜 서비스 중 하나인지 검사
        """
        if value not in getattr(settings, 'PROVIDER_LIST'):
            raise ValidationError("지원하지 않는 소셜 서비스입니다.")
        return value

    def create(self, validated_data):
        # create social_user
        user_data = validated_data.pop('user')
        try:
            social_user = super().create(validated_data)
        except IntegrityError as error:
            raise error
        else:
            user_data['id'] = social_user.id
            user_create_url = getattr(settings, 'USER_API_BASE_URL') + 'user/users'
            response = requests.post(user_create_url, json=user_data)
            response.raise_for_status()

            return social_user
